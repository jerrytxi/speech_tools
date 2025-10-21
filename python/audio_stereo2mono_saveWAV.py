import os
import parselmouth

# Define input and output folders
input_folder = "input_folder_path"
output_folder = "output_folder_path"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".mp3") and not filename.startswith("._"):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + "mono.wav"
        output_path = os.path.join(output_folder, output_filename)

        try:
            print(f"Processing: {filename}")
            
            # Load the MP3 file
            sound = parselmouth.Sound(input_path)
            
            # Convert stereo to mono
            mono_sound = sound.convert_to_mono()
            
            # Save as WAV
            mono_sound.save(output_path, "WAV")
            print(f"Saved: {output_filename}")
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")
