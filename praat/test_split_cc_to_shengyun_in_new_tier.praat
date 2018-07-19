form Convert Chinese syllable to Shen Yun
	integer source_Tier 2
	sentence target_Tier_Name shengyun
endform
clearinfo
shengyunTierName$=target_Tier_Name$
sTier=source_Tier

maxTierNum=Get number of tiers
tTier=maxTierNum+1
Insert interval tier... tTier 'shengyunTierName$'
lastT1=0
int=Get number of intervals... 'sTier'
for k from 1 to 'int'
	label$ = Get label of interval... 'sTier' 'k'
	if label$ <> "sil" and label$ <> "pause" and label$ <> ""
		startT1=Get starting point... 'sTier' 'k'
		endT1=Get end point... 'sTier' 'k'
		midT1=(endT1-startT1)/2+startT1
		
		appendInfoLine: "'startT1' 'midT1' 'endT1'"
		if startT1>lastT1 and k>1
			Insert boundary... 'tTier' 'startT1'
			lastT1=startT1
		endif
		if midT1>lastT1
			Insert boundary... 'tTier' 'midT1'
			lastT1=midT1
		endif
		if endT1>lastT1 and k<int
			Insert boundary... 'tTier' 'endT1'
			lastT1=endT1
		endif
	endif
endfor

