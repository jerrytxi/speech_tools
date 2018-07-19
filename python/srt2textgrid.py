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
if len(sys.argv)>1:
	inputSrt=sys.argv[1]
	srtFile=os.path.basename(inputSrt)
	fileName=os.path.splitext(srtFile)[0]
	fileDir=os.path.abspath(os.path.dirname(inputSrt) + os.path.sep)
	
	print(fileDir)
	srtFileObj=open(inputSrt)
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
	wordTier = tgio.IntervalTier('sentences', entryList, 0, tMax)
	tg = tgio.Textgrid()
	tg.addTier(wordTier)
	tg.save(os.path.join(fileDir,fileName + ".TextGrid"))
