#!python3
"""
   This is the entry file and script interface for string clustering.
   Implemented is a CLI akin to those of common core utilities on UNIX systems.

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

import argparse as ap
import sys

def main():
   parser = ap.ArgumentParser(
      description="Given k clusters and a set of strings, returns the strings \
                   grouped according to a chosen distance measure. The \
                   resulting output will be given back to stdout."
   )
   parser.add_argument("k", type=int, 
                       help="Specifies the number of desired groups."
   )
   parser.add_argument("infile",
         nargs="?",
         type=ap.FileType("r"),
         default=sys.stdin, 
         help="Specify the file to be read. Will read stdin by default."
   )
   parser.add_argument("-o", "--output-format",
         type=str.lower,
         choices=["csv", "text"],
         default="text",
         help="Specify the output format. Defaults to simple text format."
   )
   args = parser.parse_args()

   print("K:", args.k)
   print("output style:", args.output_format)
   print("infile:", args.infile.read())

if __name__ == "__main__":
   main()