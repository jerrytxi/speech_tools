#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  srt2textgrid.py
#  
#License: The MIT License (MIT) 
# 
#Copyright 2018 jerrytxi@gmail.com 
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
import os
import glob
import argparse
from datetime import datetime
try:
    from praatio import tgio
    from srt import parse
except ValueError:
    print("autosub not installed please run 'pip3 install srt praatio'.")


def validate(args):
    """
    Check that the CLI arguments are valid.
    """
    if not args.source_path:
        print("Error: You need to specify a source path.")
        return False
    else:
        if not os.path.exists(args.source_path):
            print("Error: Source path is not a folder or file.")
            return False       

    return True  

def srtToGrid(srtFile,outputFile):
    srtFileObj=open(srtFile)
    subs = parse(srtFileObj.read())
    entryList=[]
    tMax=0
    for sub in subs:
        startTime=sub.start.total_seconds()
        endTime=sub.end.total_seconds()
        label=sub.content
        intTier=(startTime,endTime,label)
        entryList.append(intTier)
        tMax=endTime
    srtFileObj.close()

    print("Save TextGrid to {output} ".format(output=outputFile))
    tierName="Sentences"
    if os.path.isfile(outputFile):
        tg = tgio.openTextgrid(outputFile)
        if tierName in tg.tierDict:
            tierName=tierName+datetime.now().strftime("%m%d%Y%H%M%S")
    else:
        tg = tgio.Textgrid()    
    wordTier = tgio.IntervalTier(tierName, entryList, 0, tMax)
    tg.addTier(wordTier)
    tg.save(outputFile)

	
def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help="Path to the srt file to textGrid.\
    You can use autosub to generate src from a wav file.",nargs='?')
    parser.add_argument('-o', '--output',help="Output path for subtitles (by default, \
    TextGrid are saved in the same directory and name as the source path)")
    args = parser.parse_args()
    if not validate(args):
        return 1

    if os.path.isfile(args.source_path):
        #source path is a file
        base = os.path.splitext(args.source_path)[0]
        srtFile= "{base}.{format}".format(base=base, format='srt')
        srtFileExsist=os.path.isfile(srtFile)
        if not srtFileExsist:
            print("Error:srt file is not exsist.")
            return 1
        else:
            outputFile=args.output
            if not outputFile:
                outputFile = "{base}.{format}".format(base=base, format='TextGrid')
            srtToGrid(srtFile,outputFile)
    
    else:
        #source path is a dir
        folder=os.path.dirname(args.source_path)
        srtFiles = glob.glob(os.path.join(folder, '*.srt'))
        for srtFile in srtFiles:
            base = os.path.splitext(srtFile)[0]
            outputFile = "{base}.{format}".format(base=base, format='TextGrid')
            srtToGrid(srtFile,outputFile)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
