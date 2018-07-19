# This Praat script will get average intensity, minimal intensity, and maximal intensity (in dB) of all labeled intervals of all (or a specified set of) files in a folder.
# To use, you specifiy a folder with wav.files, and base names if you want to analyze only a subset of files.
# The script assumes that you already have labeled intervals. The textgrid files and sound files should have the same name.
# Written by Shigeto Kawahara.
# version 2/10/2010

form Get Intensity
	sentence Directory ./
	comment If you want to analyze all the files, leave this blank
	word Base_file_name
	comment The name of result file
	text textfile intensity_list.txt
endform

#Print one set of headers

fileappend "'textfile$'" File name'tab$'Interval name'tab$'Avg Int'tab$'Min Int'tab$'Min Int Time'tab$'Max Int'tab$'Max Int time'tab$'
fileappend "'textfile$'" 'newline$'

#Read all files in a folder

Create Strings as file list... wavlist 'directory$'/'base_file_name$'*.wav
Create Strings as file list... gridlist 'directory$'/'base_file_name$'*.TextGrid
n = Get number of strings

tab$=','
for i to n
clearinfo
#We first extract intensity tiers
	select Strings wavlist
	filename$ = Get string... i
	Read from file... 'directory$'/'filename$'
	soundname$ = selected$ ("Sound")
	To Intensity... 100 0


	labelline$ = "'soundname$''tab$'"


# We now read grid files and extract all intervals in them
	select Strings gridlist
	gridname$ = Get string... i
	Read from file... 'directory$'/'gridname$'
	int=Get number of intervals... 1

# We calculate intensity for all labeled intervals
for k from 1 to 'int'
	select TextGrid 'soundname$'
	label$ = Get label of interval... 1 'k'
	if label$ <> ""
		# We print out the file names
		fileappend "'textfile$'" 'labelline$'
		# calculates the onset and offset
 		onset = Get starting point... 1 'k'
  		offset = Get end point... 1 'k'

		#calculates the intensity values
		select Intensity 'soundname$'
		min_int = Get minimum... onset offset Parabolic
		min_time = Get time of minimum... onset offset Parabolic
		max_int = Get maximum... onset offset Parabolic
		max_time = Get time of maximum... onset offset Parabolic
		meanIntensity = Get mean... onset offset dB
		resultline$ = "'label$''tab$''meanIntensity''tab$''min_int''tab$''min_time''tab$''max_int''tab$''max_time''tab$''newline$'"
		fileappend "'textfile$'" 'resultline$'
	endif
endfor

endfor

# clean up

select all
Remove
