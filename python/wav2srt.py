#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  wav2srt.py
# 
#License: The MIT License (MIT) 
# 
#Copyright 2020 jerrytxi@gmail.com 
#
#Permission is hereby granted, free of charge, to any person obtaining 
#a copy of this software and associated documentation 
#files (the "Software"), to deal in the Software without restriction, 
#including without limitation the rights to #use, copy, modify, merge, 
#publish, distribute, sublicense, and/or sell copies of the Software, 
#and to permit persons to whom the Software is furnished to do so, 
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included
 #in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
#OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
#IN NO EVENT SHALL THE AUTHORS OR #COPYRIGHT HOLDERS BE LIABLE FOR ANY 
#CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
#TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import argparse
import os
import glob
try:
    import autosub
except ValueError:
    print("autosub not installed please run 'pip install autosub'.")
        
def validate(args):
    """
    Check that the CLI arguments are valid.
    """
    if not args.source_path:
        print("Error: You need to specify a source path.")
        return False
    else:
        if not os.path.isdir(args.source_path):
            print("Error: Source path is not a folder.you can run autosub direct.")
            return False       

    return True   
def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help="Path to the video or audio file to subtitle",
                        nargs='?')
    parser.add_argument('-S', '--src-language', help="Language spoken in source file",
                        default="zh-CN")
    parser.add_argument('--list-languages', help="List all available source/destination languages",
                        action='store_true')

    args = parser.parse_args()
    if args.list_languages:
        os.system("autosub  --list-languages")
        return 0

    if not validate(args):
        return 1
    wavFiles = glob.glob(os.path.join(args.source_path, '*.wav'))
    for wavFile in wavFiles:
        print("autosub '{wavFile}' -S {lang} -D {lang}".format(wavFile=wavFile,lang=args.src_language))
        os.system("autosub '{wavFile}' -S {lang} -D {lang}".format(wavFile=wavFile,lang=args.src_language))
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
