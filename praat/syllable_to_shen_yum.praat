form Convert Chinese syllable to Shen Yun
	integer source_Tier_of_syllable 2
	integer target_Tier_of_sheng_yun 3
endform

clearinfo
sTier=source_Tier_of_syllable
tTier=target_Tier_of_sheng_yun
int=Get number of intervals... 'sTier'
currentTg$=selected$("TextGrid")

;call python to create table file of sheng yun mu

temp$=""
for k from 1 to 'int'
	cc$= Get label of interval... 'sTier' 'k'
	if cc$ = "sil" or cc$="pause" or cc$ = "" or cc$ = "s"
		cc$=" "
	endif
	label$[k] =cc$
	temp$=temp$+cc$
endfor
runSystem: "python3 ../python/cc2shengyun.py """,temp$,""" >temp"

;read sheng yun mu to 2 array

Read Table from comma-separated file: "temp"
rows=Get number of rows
for a from 1 to 'rows'
	shengmu$[a]=Get value... 'a' shengmu
	yunmu$[a]=Get value... 'a'  yunmu
endfor
Remove

;fill sheng yun mu to TextGrid
selectObject: "TextGrid 'currentTg$'"
for k from 1 to 'int'
	label$ = Get label of interval... 'sTier' 'k'
	startT1=Get starting point... 'sTier' 'k'
	endT1=Get end point... 'sTier' 'k'
	shenmuIndex=Get high interval at time... 'tTier'  'startT1'
	yunmuIndex=Get low interval at time... 'tTier'   'endT1'
	if label$ <> "sil" and label$ <> "pause" and label$ <> "" and label$ <> "s"
		;Get shengmu and set to shenmu interval
		sm$=shengmu$[k]
;		appendInfoLine: "Shengmu of  ",label$, " is: ", sm$
		Set interval text... 'tTier'  'shenmuIndex' 'sm$'


		ym$=yunmu$[k]
;		appendInfoLine: "Yunmu of  ",label$, " is: ", ym$
		Set interval text... 'tTier'  'yunmuIndex' 'ym$'

		appendInfoLine: "pingying of  ",label$, " is: ", sm$,ym$
	endif
endfor
deleteFile: "temp"
