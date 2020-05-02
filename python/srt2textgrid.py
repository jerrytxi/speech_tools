#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  src2textgrid.py
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
import os.path
from praatio import tgio
from datetime import timedelta
from srt import parse
import sys
import argparse
def validate(args):
    """
    Check that the CLI arguments are valid.
    """
    if not args.source_path:
        print("Error: You need to specify a source path.")
        return False

    return True    
 

	
def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help="Path to the srt file to textGrid.\
    You can use autosub to generate src from a wav file.",nargs='?')
    parser.add_argument('-o', '--output',help="Output path for subtitles (by default, \
    TextGrid are saved in the same directory and name as the source path)")
    args = parser.parse_args()
    if not validate(args):
        return 1
    base = os.path.splitext(args.source_path)[0]
    srtFile= "{base}.{format}".format(base=base, format='srt')
    isFile=os.path.isfile(srtFile)
    if not isFile:
        srtFile= "{base}.{format}".format(base=base, format='SRT')
        isFile=os.path.isfile(srtFile)
    
    if isFile:
        srtFileObj=open(srtFile)
        subs = parse(srtFileObj.read())
        outputFile=args.output
        if not outputFile:
            outputFile = "{base}.{format}".format(base=base, format='TextGrid')
            
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
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
