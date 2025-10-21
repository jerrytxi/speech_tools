# This script is used to automate the process of extracting specific tiers from TextGrid files, to start prosody annotation (syllable, ToBI).
# This script work on taks below:
# 1. Extract tiers: s2tCheck, utterance
# 2. Adding one blank tier: noteWord
# 3. Save new textgrid with the original name
# 4. Rename original TextGrid files by adding a prefix
###
# It uses the praatio library for handling TextGrid files.
# Python version: 3.9.6
# praatio 6.2.0 (2025-07-28 created by cps, with ChatGPT)

import os
from praatio import textgrid


def extract_two_tiers_from_folder(input_folder, output_folder, tier_names,
                                   include_empty_intervals=True,
                                   textgrid_format="short_textgrid"):
    """
    Processes all TextGrid files in a folder, extracting specified tiers
    and adding a blank 'noteWord' tier.

    Args:
        input_folder (str): Directory containing input TextGrid files.
        output_folder (str): Directory to save output TextGrid files.
        tier_names (List[str]): Names of tiers to extract.
        include_empty_intervals (bool): Whether to include empty intervals.
        textgrid_format (str): Format to save ("short_textgrid", "long_textgrid", "json", "textgrid_json").
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".TextGrid") and not filename.startswith("._"):
            input_tg_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".TextGrid"   #use the same name
            output_tg_path = os.path.join(output_folder, output_filename)

            try:
                tg = textgrid.openTextgrid(input_tg_path, includeEmptyIntervals=include_empty_intervals)

                # Validate requested tiers
                existing_tier_names = tg._tierDict
                missing = [name for name in tier_names if name not in existing_tier_names]
                if missing:
                    print(f"Skipping {filename}: Tiers not found: {missing}")
                    continue

                # Create new TextGrid
                new_tg = textgrid.Textgrid()
                new_tg.minTimestamp = tg.minTimestamp
                new_tg.maxTimestamp = tg.maxTimestamp

                # Add specified tiers
                for name in tier_names:
                    tier = tg.getTier(name)
                    new_tg.addTier(tier)

                # Add blank 'noteWord' tier
                blank_interval = [(tg.minTimestamp, tg.maxTimestamp, "")]
                new_tier = textgrid.IntervalTier('noteWord', blank_interval, tg.minTimestamp, tg.maxTimestamp)
                new_tg.addTier(new_tier)

                # Save output
                new_tg.save(output_tg_path,
                            format=textgrid_format,
                            includeBlankSpaces=include_empty_intervals)

                print(f"Processed: {filename}")


            except Exception as e:
                print(f"Error processing {filename}: {e}")


# Complete extract and save new TextGrid, rename old files with adding prefix
def rename_original_file_adding_prefix(input_folder):
    num_file = 0
    print(f"------------\n"
          f"Renaming files in {input_folder}...\n")
    prefix_to_add = input("Enter the prefix to add (e.g. z-S2T_): ")
    for filename in os.listdir(input_folder): 
        if filename.endswith(".TextGrid") and not filename.startswith("._"):
            old_path = os.path.join(input_folder, filename)

            # Skip directories
            if os.path.isfile(old_path):    
                new_filename = prefix_to_add + filename
                new_path = os.path.join(input_folder, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} → {new_filename}")
                num_file += 1
        print(f"Total files renamed (added prefix): {num_file}")


# run this script
if __name__ == "__main__":
    input_folder="/Users/cps/Desktop/0-tokenlisation/temp_input_folder/"
    output_folder="/Users/cps/Desktop/0-tokenlisation/temp_output_folder/"
    tier_names=["s2tCheck", "utterance"]
    extract_two_tiers_from_folder(input_folder, output_folder, tier_names,
                                   include_empty_intervals=True,
                                   textgrid_format="short_textgrid")
    rename_original_file_adding_prefix(input_folder)