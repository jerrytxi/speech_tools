# This script duplicates a specified tier in all TextGrid files within a given folder.
# It uses the praatio library to handle TextGrid files.
# duplicate tier: tier 2 (index 1) to a new tier named "utterance" at index 2.
# This script is use to automate the process of duplicating tiers in TextGrid files, before determining utterance boundaries.
#  (2025-07-28 created by cps, with Gemini)

from praatio import textgrid
import os

def duplicate_tier_in_folder(input_folder, output_folder, source_tier_index, new_tier_name, insert_index=None):
    """
    Duplicates a tier specified by its index in all TextGrid files within an input folder
    and saves the modified TextGrids to an output folder.
    The duplicated tier can be inserted at a specific position.

    Args:
        input_folder (str): The path to the folder containing input TextGrid files.
        output_folder (str): The path to the folder where modified TextGrid files will be saved.
        source_tier_index (int): The 0-based index of the tier to duplicate.
        new_tier_name (str): The name for the duplicated tier.
        insert_index (int, optional): The index (0-based) where the new tier should be inserted.
                                      If None, the tier is added to the end. Defaults to None.
    """

    print(f"Processing TextGrid files in: {input_folder}")
    print(f"Saving modified TextGrids to: {output_folder}")
    print(f"Duplicating tier at index '{source_tier_index}' to '{new_tier_name}'")
    if insert_index is not None:
        print(f"Inserting new tier at index: {insert_index}")
    print("\n")

    processed_count = 0
    skipped_count = 0

    for filename in os.listdir(input_folder):
        if filename.endswith(".TextGrid"):
            input_textgrid_path = os.path.join(input_folder, filename)
            output_textgrid_path = os.path.join(output_folder, filename)

            try:
                # Load the TextGrid
                tg = textgrid.openTextgrid(input_textgrid_path, includeEmptyIntervals=False)

                # Check if the source tier index is valid
                if not (0 <= source_tier_index < len(tg.tiers)):
                    print(f"  Skipping '{filename}': Source tier index {source_tier_index} is out of bounds (0-{len(tg.tiers)-1}).")
                    skipped_count += 1
                    continue

                # Get the source tier by index
                source_tier = tg.tiers[source_tier_index] 
                # print(f"  Source tier name for '{filename}': {source_tier.name}") # Optional: verify tier name

                # Create a new tier with the same content as the source tier
                duplicated_tier = source_tier.new(name=new_tier_name)

                # Add the duplicated tier to the TextGrid at the specified index
                tg.addTier(duplicated_tier, tierIndex=insert_index)

                # Save the modified TextGrid
                tg.save(output_textgrid_path, format="short_textgrid", includeBlankSpaces=True)
                print(f"  Processed '{filename}': Tier '{source_tier_index}' duplicated to '{new_tier_name}'.")
                processed_count += 1

            except Exception as e:
                print(f"  Error processing '{filename}': {e}")
                skipped_count += 1
        else:
            print(f"  Skipping '{filename}': Not a TextGrid file.")

    print(f"\n--- Summary ---")
    print(f"Total TextGrid files processed: {processed_count}")
    print(f"Total files skipped (not TextGrid or tier not found/error): {skipped_count}")
    print(f"Processing complete.")


if __name__ == "__main__":
    # --- Example Usage ---

    # 1. Create a dummy TextGrid for demonstration
    # In a real scenario, you would have an existing TextGrid file.
    # We'll create a simple one here.
    input_dir = "/Users/cps/Desktop/0-tokenlisation/textGrid_s2t/"
    output_dir = "/Users/cps/Desktop/0-tokenlisation/output_textgrids_folder/"

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    

    # 2. Call the function to duplicate a tier
    source_tier_index = 1
    new_tier_name = "utterance"
    target_insert_index = 2
    duplicate_tier_in_folder(input_dir, output_dir, source_tier_index, new_tier_name, target_insert_index)

    print(f"\nCheck the '{output_dir}' folder for the processed TextGrids.")
    # You can now open 'my_audio_duplicated_tier.TextGrid' in Praat
    # to see the duplicated tier.