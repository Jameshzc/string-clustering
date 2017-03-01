#!python3
"""
Contains the classes relevant to the clustering implementation. Currently
implemented is k-means clustering adapted for a non-euclidean distance measure,
which is known as k-medoids clustering. Using the same interface, other
clustering techniques can be implemented.

Copyright 2017 Eric Yi-Hsun Huang (Kris Wallperington)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import random
import stringdist
import collections
from pprint import pprint

class DistanceMatrix(object):
   """
   Stores the distances between elements in our set. This allows us to avoid
   unnecessary recomputation of the distance, and instead we can precompute
   and store the result. To avoid floating point error, distances are rounded
   to 6 decimal places.

   If necessary, this provides the API that would allow
   for the storage method to be swapped out (i.e. writing the distances to disk
   if the number of elements is very large). The implementation has been
   optimized by only storing one-way distances, since a distance matrix is
   always symmetrical.
   """

   def __init__(self, elems, distanceFunc):
      """
      elems
         A elements to perform distance calculation on. Must be hashable.
      distanceFunc
         The function used to evaluate the distance between two
         elements. We assume that 0 represents a completely dissimilar result,
         and that 1 represents a strongly similar result.
      """

      # Copy elements, so that a change in the original list doens't affect us.
      # Initializes the first layer of the matrix to empty dictionary.
      self.distMap = {e:{} for e in elems}
      self.getDist = distanceFunc


      for first in elems:
         for second in elems:
            # Check if reverse direction exists - if it does, don't store
            if self.distMap.get(second).get(first) is None:
               self.distMap[first][second] = round(self.getDist(first, second), 6)

   def dist(self, elem_a, elem_b):
      """
      Returns the distance from elem_a to elem_b, or -1 if either element
      is not present in the matrix.
      """

      # Default to empty dict in case the key doesn't exist to simplify
      # return logic
      direct_dist = self.distMap.get(elem_a, {}).get(elem_b)
      if direct_dist is None:
         reverse_dist = self.distMap.get(elem_b, {}).get(elem_a)
         if reverse_dist is None:
            # No entry stored for this pair - error out
            return -1

         # Found reverse mapping
         return reverse_dist

      # Found direct mapping
      return direct_dist

class ClusterEngine(object):
   """
   Class to perform clustering. This class provides an interface similar to
   those of builders. Any attempt to materialize the result before clustering
   has been performed will result in an exception.
   """

   def __init__(self, k, elems):
      self.k = k
      self.elems = elems
      # When set, will be a list of lists, 
      # where each inner list represents a group.
      self.result = None
      self.distMat = DistanceMatrix(self.elems, stringdist.jaroWinklerDistance)

   def cluster(self):
      if not self.elems:
         # We choose to return an exception in the event no elements are given.
         # This could easily be changed to return an empty result, instead.
         raise ValueError("Cannot cluster an empty set!")

      # We sample k starting points (without replacement) to use as the seed
      # groups. We set these as our starting groups. The index of each element
      # is implicitly the group defined by that element.
      current_medoids = random.sample(self.elems, self.k)

      # Track the last set of medoids used. Our exit condition is when we
      # pick new medoids that are the same as the last.
      last_medoids = None

      # We check similarity using a counter to do an order-insensitive equality.
      while collections.Counter(last_medoids) != \
            collections.Counter(current_medoids):
         # print("Current medoids:\n{}".format(current_medoids))
         # Wipe the results, and re-seed based on the medoids
         self.result = []
         for m in current_medoids:
            self.result.append([m])

         # Assignment: Assign each element to the group that it has the closest
         # distance to.
         for e in self.elems:
            # Only consider elements not a medoid
            if e not in current_medoids:
               # If there is a tie, then the earlier group would be picked.
               # We could extend this to do a random tie breaker instead if
               # we wanted.

               # This computes the distance from each medoid to e
               e_dists = [self.distMat.dist(m, e) for m in current_medoids]
               closest_group_idx = e_dists.index(max(e_dists))
               self.result[closest_group_idx].append(e)

         last_medoids = current_medoids[:]
         current_medoids = [self.findNewMedoid(group) for group in self.result]

      # When we fall through, self.result is clustered with the locally
      # optimal groupings, and we return ourselves to allow function chaining.
      return self

   def findNewMedoid(self, group):
      """
      Given a group as a list, figure out the element that maximizes our
      similiary measurement and return it.

      For each element m, we calculate the sum of the distance between m and
      each element e. The biggest result is the element that has the best
      similarity, and is chosen to be returned as the next medoid.
      """
      # pprint(group)

      each_sum_dists = [sum((self.distMat.dist(m, e) for e in group)) for m in group]
      # for m in group:
         # print("m:{}\n\t{}".format(m, sum((self.distMat.dist(m, e) for e in group))))
      best_medoid = group[each_sum_dists.index(max(each_sum_dists))]

      return best_medoid

   def asCSV(self):
      if not self.result:
         raise InvalidStateError("This cannot be called before the result is materialized!")

   def asText(self):
      if not self.result:
         raise InvalidStateError("This cannot be called before the result is materialized!")

      output = ""
      for i,group in enumerate(self.result):
         output += "Group {}:\n".format(i)
         for e in group:
            output += "\t{}\n".format(e)

      return output

class InvalidStateError(Exception):
   """
   Used by ClusterEngine to represent the scenario where the user does not call
   the methods in the right order.
   """
   pass