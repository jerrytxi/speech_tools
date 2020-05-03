#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  wavsplit2textgrid.py
# 
#License: The MIT License (MIT) 
# 
#Copyright 2020 jerrytxi@gmail.com 
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
#this script depand on parselmouth praatio
#pip3 install praat-parselmouth praatio
import argparse
import os
import glob
import parselmouth
import numpy as np
from praatio import tgio
from datetime import datetime
def pitchToEntryList(pitch):
    """Get EntryList for TextGrid from a pitch object.
        Args:
            pitch (parselmouth.Pitch): pitch object by praat
        Returns:
            a list like [(startV1, endV1, label1), (startV2, endV2, label2), ...]
    """
    startTime=0.00
    endTime=0.00
    syllableOn=0
    syllableCnt=1
    entryList=[]
    for i in range(1,pitch.n_frames):
        pitchValue=pitch.get_value_in_frame(i)
        if np.isnan(pitchValue):
            if syllableOn==True:
                endTime=pitch.get_time_from_frame_number(i-1)
                if endTime > startTime:
                    entryList.append((startTime,endTime,"s"+str(syllableCnt)))
                    syllableCnt+=1
                syllableOn=False
        else:
            if syllableOn==False:
                startTime=pitch.get_time_from_frame_number(i)
                syllableOn=True
       
    return entryList
def wavFileToGrid(wavFile,outputFile):
    snd = parselmouth.Sound(wavFile)
    pitch = snd.to_pitch()
    print("Get entryList for TextGrid From {file} by pitch".format(file=wavFile))
    entryList=pitchToEntryList(pitch) 

    print("Save TextGrid to {output} ".format(output=outputFile))
    tierName="Pitch"
    if os.path.isfile(outputFile):
        tg = tgio.openTextgrid(outputFile)
        if tierName in tg.tierDict:
            tierName=tierName+datetime.now().strftime("%m%d%Y%H%M%S")
    else:
        tg = tgio.Textgrid()    
    wordTier = tgio.IntervalTier(tierName, entryList, 0, pairedWav=wavFile)
    tg.addTier(wordTier)
    tg.save(outputFile)


def validate(args):
    """
    Check that the CLI arguments are valid.
    """
    if not args.source_path:
        print("Error: You need to specify a source path.")
        return False
    else:
        if not os.path.exists(args.source_path):
            print("Error: Source path is not a folder or file.")
            return False       

    return True    

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help="Path to the wav file to textGrid",nargs='?')
    parser.add_argument('-o', '--output',help="Output path for subtitles (by default, TextGrid are saved in the same directory and name as the source path)")
    args = parser.parse_args()
    if not validate(args):
        return 1
    if os.path.isfile(args.source_path):
        #source path is a file
        base = os.path.splitext(args.source_path)[0]
        wavFile= "{base}.{format}".format(base=base, format='wav')
        wavFileExsist=os.path.isfile(wavFile)
        if not wavFileExsist:
            print("Error:Wav file is not exsist.")
            return 1
        else:
            outputFile=args.output
            if not outputFile:
                outputFile = "{base}.{format}".format(base=base, format='TextGrid')
            wavFileToGrid(wavFile,outputFile)
    else:
        #source path is a dir
        folder=os.path.dirname(args.source_path)
        wavFiles = glob.glob(os.path.join(folder, '*.wav'))
        for wavFile in wavFiles:
            base = os.path.splitext(wavFile)[0]
            outputFile = "{base}.{format}".format(base=base, format='TextGrid')
            wavFileToGrid(wavFile,outputFile)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
