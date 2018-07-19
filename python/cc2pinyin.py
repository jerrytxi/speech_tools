#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  cc2pinyin.py
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
from pypinyin import pinyin, lazy_pinyin, Style
import sys
import operator
if len(sys.argv)>1:
	input_cc=sys.argv[1]
	output_pinyin=pinyin(input_cc,8,heteronym=False)
	for cc in output_pinyin:
		#if operator.eq(cc,output_pinyin[-1]):
		if cc == output_pinyin[-1]:
			print(cc[0],end='')
		else:
			print(cc[0],end=' ')
else:
	print(' ',end='')
