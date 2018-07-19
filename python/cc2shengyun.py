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
from pypinyin import pinyin
import sys
print('syllable',end=',')
print('pinyin',end=',')
print('shengmu',end=',')
print('yunmu')

if len(sys.argv)>1:
	input_cc=sys.argv[1]
	output_pinying_list=pinyin(input_cc,8,heteronym=False)
	output_shengmu_list=pinyin(input_cc,3,heteronym=False)
	output_yunmu_list=pinyin(input_cc,9,heteronym=False)
	for i in range(len(output_shengmu_list)):
		print(input_cc[i],end=',')
		print(output_pinying_list[i][0],end=',')
		print(output_shengmu_list[i][0],end=',')
		print(output_yunmu_list[i][0])

