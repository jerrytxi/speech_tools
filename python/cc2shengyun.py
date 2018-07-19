#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  cc2pinyin.py
#  
#  Created by 周宝芯 <dianqing82@gmail.com> 18.07.2018 08:51:21 +08
from pypinyin import pinyin
import sys
if len(sys.argv)>1:
	input_cc=sys.argv[1]
	output_shengmu_list=pinyin(input_cc,3,heteronym=False)
	output_yunmu_list=pinyin(input_cc,9,heteronym=False)
	for i in range(len(output_shengmu_list)):
		print(output_shengmu_list[i][0],end=' ')
#		print(output_yunmu_list[i][0],end=' ')
		
		if output_yunmu_list[i] == output_yunmu_list[-1]:
			print(output_yunmu_list[i][0],end='')
		else:
			print(output_yunmu_list[i][0],end=' ')
else:
	print(' ',end='')
