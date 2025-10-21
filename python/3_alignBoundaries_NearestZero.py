import praatio.praatio_scripts as praat_scripts
from praatio import textgrid
from praatio import audio
import os

# --- Configuration ---
# Set the path to your folder containing audio and TextGrid files
input_folder = "/Users/cps/Desktop/0-tokenlisation/1-textGrid_s2t"
output_folder = "/Users/cps/Desktop/0-tokenlisation/2b-textGrid_forANLS"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)
tier_to_alignBoundaries = 3

# --- Process all files in the folder ---
for filename in os.listdir(input_folder):
    if filename.endswith(".TextGrid"):
        textgrid_filepath = os.path.join(input_folder, filename)
        
        # Assume audio file has the same name but with a .wav extension
        # You might need to adjust this logic if your audio files have different naming conventions
        filename_base = os.path.splitext(filename)[0]
        audio_filename_base = filename_base[:-5] + "mono"   # Remove the last 5 characters ("_ANLS")
        audio_filepath = os.path.join(input_folder, audio_filename_base + ".wav")
        #open the audio file as a Wav object
        # wav_object = praatio.audio.Wav(audio_filepath)  # This line is not
        wav_object = audio.Wav.open(audio_filepath)  
        # Check if the audio file is valid
        if not wav_object:
            print(f"Skipping {filename}: Invalid audio file {audio_filepath}.")
            continue
        # print wav file information
        wav_object.print_info()  # Uncomment this line if you want to print the wav file information

    

        # Check if the corresponding audio file exists
        if not os.path.exists(audio_filepath):
            print(f"Skipping {filename}: Corresponding audio file {audio_filepath} not found.")
            continue

        output_textgrid_filepath = os.path.join(output_folder, filename)



        print(f"Processing {filename}...")

        # 1. Load the TextGrid
        tg = textgrid.openTextgrid(textgrid_filepath, includeEmptyIntervals=True)
        
        # 2. Select the tier(s) to process
        # Get the specific tier by name. Ensure 'utterances' exists in your TextGrid.
        # If you want to process ALL tiers, you would pass tg.tierList instead.
        tiers_to_process = [tg.tiers[tier_to_alignBoundaries]] # Get the 'utterances' tier

        # 3. Call tgBoundariesToZeroCrossings with the list of tiers
        # The function now returns a NEW TextGrid object
        processed_tg = praat_scripts.tgBoundariesToZeroCrossings(
            tg, # Pass the list of tiers here
            wav_object,
            # minSilence=0.01,
            # maxSilence=0.1
        )
        
        # 4. Save the modified TextGrid
        processed_tg.save(output_textgrid_filepath)
        
        print(f"  Successfully processed and saved to: {output_textgrid_filepath}")




        # try:
        #     print(f"Processing {filename}...")
        #     praat_scripts.tgBoundariesToZeroCrossings(
        #         audio_filepath,
        #         textgrid_filepath,
        #         output_textgrid_filepath,
        #         # replace=False,  # Set to False to create new files in the output folder
        #         tierName="utterances/word", # Specify the tier name, or set to None for all tiers
        #         minSilence=0.01,
        #         maxSilence=0.1
        #     )
        #     print(f"  Successfully processed and saved to: {output_textgrid_filepath}")
        # except Exception as e:
        #     print(f"  Error processing {filename}: {e}")
        #     print("  Please ensure Praat is installed and accessible, and files are valid.")
