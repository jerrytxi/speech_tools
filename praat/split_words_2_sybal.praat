

form Split Words to Syllable 
	integer source_Tier_of_words 1
	integer target_Tier_of_syllable 2
endform
clearinfo
sTier=source_Tier_of_words
tTier=target_Tier_of_syllable
int=Get number of intervals... 'sTier'
for k from 1 to 'int'
	label$ = Get label of interval... 'sTier' 'k'
	startT1=Get starting point... 'sTier' 'k'
	endT1=Get end point... 'sTier' 'k'
	startI2=Get high interval at time... 'tTier'  'startT1'
	endI2=Get low interval at time... 'tTier'   'endT1'
	if label$ <> "sil" and label$ <> "pause" and label$ <> ""
		len=length(label$)
		for a to len
			syb$=mid$(label$,a,1)
			nowI2=startI2-1+a
			if nowI2<=endI2
				Set interval text... 'tTier'  'nowI2' 'syb$'
			endif
			appendInfoLine: "Add `"+syb$+"`to interval 'nowI2'"
		endfor
	else
		Set interval text... 'tTier'  'startI2' 'label$'
	endif
endfor