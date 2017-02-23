#!python3
"""
	This file contains the classes used to calculate string distance. A uniform
	API is exposed to make it easy to swap out which specific distance measure
	is used. Currently only Jaro-Winkler distance is implemented, but other
	algorithms worth considering include Hamming distance and Levenshtein
	distance.

	Care must be taken, as not every distance measure can be interpreted in
	the same way.

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

class StringDistance(object):
	"""
	Base class containing common functionality across all implementations.
	Should be considered abstract and not to be instantiated directly.
	"""

	def distance(string_a, string_b):
		"""
		Given two strings, returns the edit distance representing how similar
		they are.
		"""

		raise NotImplementedError()

class JaroWinkler(StringDistance):
	"""
	Concrete class implementing the Jaro-Winkler distance measure.
	"""

	def distance(string_a, string_b):
		"""
		Returns a number between 0.0 and 1.0 (inclusive), where 0.0 represents
		complete difference, and 1.0 represents an exact match.
		"""