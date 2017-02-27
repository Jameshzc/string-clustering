#!python3
"""
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

import unittest

import stringdist

class TestStringDistance(unittest.TestCase):
  """
  This class tests the same example cases as given in the reference
  Jaro-Winkler implementation. While it is not exaustive, it is assumed that
  the reference implementation is stable enough that it is sufficient to simply
  check that the two implementations agree on a few test cases.

  To better establish the correctness of the ported implementation, we could
  either link to the C++ implementation, or externally call on its executable.
  Then a more comprehensive test can be done to establish that the two
  implementations agree.

  To elegantly handle minor variances in floating point calculations, we only
  assert the match up to 6 decimal places, which should prove sufficient in
  most use cases.
  """

   def test_jaro_martha(self):
      self.assertAlmostEqual(
        stringdist.jaroDistance("MARTHA", "MARHTA"), 0.944444, places=6
      )

   def test_jaro_winkler_martha(self):
      self.assertAlmostEqual(
         stringdist.jaroWinklerDistance("MARTHA", "MARHTA"), 0.961111, places=6
      )

   def test_jaro_dwayne(self):
      self.assertAlmostEqual(
        stringdist.jaroDistance("DWAYNE", "DUANE"), 0.822222, places=6
      )

   def test_jaro_winkler_dwayne(self):
      self.assertAlmostEqual(
        stringdist.jaroWinklerDistance("DWAYNE", "DUANE"), 0.84, places=6
      )

   def test_jaro_dixon(self):
      self.assertAlmostEqual(
        stringdist.jaroDistance("DIXON", "DICKSONX"), 0.766667, places=6
      )

   def test_jaro_winkler_dixon(self):
      self.assertAlmostEqual(
        stringdist.jaroWinklerDistance("DIXON", "DICKSONX"), 0.813333, places=6
      )

if __name__ == '__main__':
   unittest.main()
