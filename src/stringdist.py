#!python3
"""
This file contains the functions used to calculate string distance. The same
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

# Configurable weights and constants for Jaro and Jaro-Winkler
JARO_WEIGHT_STRING_A = 1.0/3.0
JARO_WEIGHT_STRING_B = 1.0/3.0
JARO_WEIGHT_TRANSPOSITIONS = 1.0/3.0

JARO_WINKLER_PREFIX_SIZE = 4
JARO_WINKLER_SCALING_FACTOR = 0.1
JARO_WINKLER_BOOST_THRESHOLD = 0.7

def jaroDistance(string_a, string_b):
	"""
	Given two strings, returns the jaro distance between them.
	"""

	a_len = len(string_a)
	b_len = len(string_b)

	if 0 == a_len or 0 == b_len:
		# One of the strings is empty, must return no similarity
		return 0.0

	# Max length, as part of the definition of Jaro Distance
	max_range = max(0, max(a_len, b_len) // 2 - 1)

	# Arrays that represent whether or not the character
	# at the specified index is a match
	a_match = [False] * a_len
	b_match = [False] * b_len

	char_matches = 0
	for a_idx in range(a_len):
		# Represents the sliding window we use to determine matches
		min_idx = max(a_idx - max_range, 0)
		max_idx = min(a_idx + max_range + 1, b_len)

		if min_idx >= max_idx:
			# Means we ran past the end of string b - nothing left to compare
			break

		for b_idx in range(min_idx, max_idx):
			if not b_match[b_idx] and string_a[a_idx] == string_b[b_idx]:
				# Found a new match
				a_match[a_idx] = True
				b_match[b_idx] = True
				char_matches += 1
				break	

	if 0 == char_matches:
		# If no characters match, then we must return 0.
		return 0.0

	a_pos = [0] * char_matches
	b_pos = [0] * char_matches

	pos_idx = 0
	for a_idx in range(a_len):
		if a_match[a_idx]:
			a_pos[pos_idx] = a_idx
			pos_idx += 1

	pos_idx = 0
	for b_idx in range(b_len):
		if b_match[b_idx]:
			b_pos[pos_idx] = b_idx
			pos_idx += 1

	transpositions = 0
	for i in range(char_matches):
		if string_a[a_pos[i]] != string_b[b_pos[i]]:
			transpositions += 1

	return \
		JARO_WEIGHT_STRING_A * char_matches / a_len + \
		JARO_WEIGHT_STRING_B * char_matches / b_len + \
		JARO_WEIGHT_TRANSPOSITIONS * (char_matches - transpositions // 2) \
		/ char_matches

def jaroWinklerDistance(string_a, string_b):
	"""
	Given two strings, returns their similarity as a float between 0.0 and 1.0.

	This method depends on Jaro distance.
	"""
	distance = jaroDistance(string_a, string_b)

	if distance > JARO_WINKLER_BOOST_THRESHOLD:
		common_prefix = 0
		end_idx = min(len(string_a), len(string_b), JARO_WINKLER_PREFIX_SIZE)
		for i in range(end_idx):
			if string_a[i] == string_b[i]:
				common_prefix += 1
			else:
				break

		distance += JARO_WINKLER_SCALING_FACTOR * common_prefix * \
					(1.0 - distance)

	return distance