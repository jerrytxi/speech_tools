#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  src2textgrid.py
#  
#  Copyright 2018 Taoxi <jerrytxi@gmail.com>
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
