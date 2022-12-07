#!/usr/bin/env python3
# file interval
# finds the intervals for the textgrid
import sys
import parselmouth
import tgt
import numpy as np
import math
import argparse
import glob
import os
parser = argparse.ArgumentParser(
                    prog = 'soundfile textgrid generator',
                    description = 'Generate Textgrid')

parser.add_argument('file',help = 'wav file/folder to process')
DEFAULT_WINDOW_SIZE = 0.02
DEFAULT_INTENSITY_TRESHOLD = 59
MIN_SYLB = 6*0.02
MIN_PAUSE = 50 *0.02

def check_sound_frames_intensity(sound,window_size=DEFAULT_WINDOW_SIZE,intensity_treshold=DEFAULT_INTENSITY_TRESHOLD):
    sound_end_time = sound.get_end_time()
    frame_times = []
    results = []
    for count in range(0, int(sound_end_time//window_size)):
        frame_times.append((count*window_size, count*window_size + window_size))
    if sound_end_time % window_size != 0:
        frame_times.append((count*window_size, sound_end_time))
        
    for index,time in enumerate(frame_times):
        sound_frame  = sound.extract_part(time[0], time[1])
        intensity = sound_frame.get_intensity()
        results.append((index, intensity > intensity_treshold))
    return results


def join_consecutive_bools(results,window_size=DEFAULT_WINDOW_SIZE):
    last = False
    # points = []
    temp_hold = []
    parts = []
    for index, result in results:
        if result == True and last == False:
            # start
            temp_hold.append(index*window_size)
        elif result == False and last == True:
            # End
            temp_hold.append(index*window_size)
            parts.append(temp_hold[:])
            temp_hold.clear()
        last = result
    if temp_hold:
        temp_hold.append(index*window_size)
        parts.append(temp_hold)
    return parts

def remove_noise_parts(parts):
    # print(len(parts))
    #remove short parts
    for index,part in enumerate(parts):
        if part[1] - part[0] < MIN_SYLB:
            del parts[index]
    return parts
def merge_close_parts(parts):
    # remove short stops
    lastlenght = len(parts)
    lenght = 0
    while lastlenght != lenght:
        for index,part in enumerate(parts):
            if index == len(parts) -1:
                break
            next_part = parts[index+1]
            if next_part[0] - part[1] < MIN_PAUSE:
                parts[index][1] = next_part[1]
                del parts[index+1]
        lastlenght = lenght
        lenght = len(parts)
    return parts

def remove_pitchless_parts(sound,parts):
    for index,part in enumerate(parts):
        sound_part = sound.extract_part(part[0],part[1])
        try:
            pitched = sound_part.to_pitch()
            slope = pitched.get_mean_absolute_slope()
        except parselmouth.PraatError:
            del parts[index]
        else:
            if pitched.count_voiced_frames() == 0:
                del parts[index]
            elif math.isnan(slope):
                del parts[index]
    return parts



def write_textgrid(parts):
    txtGrid_obj = parselmouth.TextGrid(0, parts[-1][1], ['auto_word']).to_tgt()
    word = txtGrid_obj.get_tier_by_name('auto_word')
    for start,end in parts:
        word.add_annotation(tgt.core.Interval(start,end, 'l'))
    final_textgrid = parselmouth.TextGrid.from_tgt(txtGrid_obj)

    return final_textgrid

def file_to_textgrid_pipeline(filename):
    print('Processing',filename)
    sound = parselmouth.Sound(filename)
    frames = check_sound_frames_intensity(sound)
    # with open('debug.txt','w') as debug:
    #     print(frames,file=debug)
    # print(frames)
    parts = join_consecutive_bools(frames)
    # print(parts)
    parts = remove_noise_parts(parts)
    parts = merge_close_parts(parts)
    parts = remove_pitchless_parts(sound,parts)
    # print(parts)
    if len(parts)==0:
        print("NO SOUND")
        return
    print("LEN:",len(parts))
    final_textgrid = write_textgrid(parts)
    final_filename = filename[:-3] + 'TextGrid'
    final_textgrid.save(final_filename)
    return final_filename,parts

def main():
    args = parser.parse_args()
    file = args.file
    
    if os.path.isfile(file):
        file_to_textgrid_pipeline(file)
    elif os.path.isdir(file):
        all_wavs = glob.glob(os.path.join(file,'*.wav'))
        for file in all_wavs:
            file_to_textgrid_pipeline(file)

if __name__ == '__main__':
    sys.exit(main())