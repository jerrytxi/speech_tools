#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  cc2pinyin.py
#  
#  Created by 周宝芯 <dianqing82@gmail.com> 18.07.2018 08:51:21 +08
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
