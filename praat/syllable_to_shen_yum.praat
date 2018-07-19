form Convert Chinese syllable to Shen Yun
	integer source_Tier_of_syllable 2
	integer target_Tier_of_sheng_yun 3
endform
clearinfo
sTier=source_Tier_of_syllable
tTier=target_Tier_of_sheng_yun
int=Get number of intervals... 'sTier'
for k from 1 to 'int'
	label$ = Get label of interval... 'sTier' 'k'
	startT1=Get starting point... 'sTier' 'k'
	endT1=Get end point... 'sTier' 'k'
	shenmuIndex=Get high interval at time... 'tTier'  'startT1'
	yunmuIndex=Get low interval at time... 'tTier'   'endT1'
	if label$ <> "sil" and label$ <> "pause" and label$ <> ""
		;Get shengmu and set to shenmu interval
		runSystem: "python3 ../python/cc2shengmu.py ",label$,">temp"
		shengmu$ = readFile$ ("temp")
		Set interval text... 'tTier'  'shenmuIndex' 'shengmu$'
		
		appendInfoLine: "Shengmu of  ",label$, " is: ", shengmu$

		;Get yunmu and set to shenmu interval
		runSystem: "python3 ../python/cc2yunmu.py ",label$,">temp"
		yunmu$ = readFile$ ("temp")
		Set interval text... 'tTier'  'yunmuIndex' 'yunmu$'

		appendInfoLine: "Yunmu of  ",label$, " is: ", yunmu$
	endif
endfor
deleteFile: "temp"
