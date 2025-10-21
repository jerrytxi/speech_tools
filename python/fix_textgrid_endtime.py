# This script fixes the end time of intervals in a TextGrid file to match the audio file duration.
# It changes the end time of the last interval in each tier to the duration of the corresponding audio file.
# Use Praatio version 6.2.0 (2025-08-12 created by cps, with ChatGPT)

from praatio import textgrid
from pydub import AudioSegment
import os


def batch_update_textgrids(input_folder, output_folder):
    print(f"{'File':30} {'Original':>10} {'Updated':>12}")
    print("-" * 55)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".textgrid"):
            base = os.path.splitext(filename)[0]
            tg_path = os.path.join(input_folder, filename)
            wav_path = os.path.join(input_folder, base + ".wav")
            
            if os.path.exists(wav_path):
                update_textgrid_times(tg_path, wav_path, output_folder)
            else:
                print(f"⚠ No matching wav for {filename}")


def update_textgrid_times(textgrid_path, wav_path, output_folder):
    # Load original TextGrid
    print(f'textgrid_path: {textgrid_path}')
    tg = textgrid.openTextgrid(textgrid_path, includeEmptyIntervals=True)
    original_max_time = tg.maxTimestamp
    
    # Get wav duration (seconds)
    audio = AudioSegment.from_file(wav_path)
    wav_duration = len(audio) / 1000.0  # ms → seconds
    
    # Update global max time
    tg.maxTimestamp = wav_duration
    
    # Update last interval xmax for each tier
    for tier_name in tg.tierNames:
        tier = tg.getTier(tier_name)
        
        if isinstance(tier, textgrid.IntervalTier) and tier.entries:
            entries = list(tier.entries)
            start_time, _, label = entries[-1]
            entries[-1] = (start_time, wav_duration, label)
            tier = textgrid.IntervalTier(tier_name, entries, wav_duration)
        
        elif isinstance(tier, textgrid.PointTier):
            tier.maxTimestamp = wav_duration
        
        tg.replaceTier(tier_name, tier)
    
    # Save updated TextGrid in new folder
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, os.path.basename(textgrid_path))
    tg.save(output_path, format="short_textgrid", includeBlankSpaces=True)
    
    # Print comparison
    print(f"{os.path.basename(textgrid_path):30} "
          f"{original_max_time:8.3f} sec → {wav_duration:8.3f} sec")




if __name__ == "__main__":
    input_folder = "/Users/cps/Desktop/0-tokenlisation/temp_input_folder/"
    output_folder = "/Users/cps/Desktop/0-tokenlisation/temp_output_folder/"
    batch_update_textgrids(input_folder, output_folder)