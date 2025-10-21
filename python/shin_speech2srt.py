#This script is used to call Whisper model to execute speech-to-text task
#mainly transribing Chinese speech
#the transcription will be saved in srt format,
#and then transfer to textgrid format for phonetic analysis.
#This script will repeat the tasks above for all audio files and srt files in the same folder.
#created by dianqing82@gmail.com, 2025 (version 2025-03-05)


#import whisper

# 加载 Whisper 模型（可选 "tiny", "base", "small", "medium", "large"）
#model = whisper.load_model('turbo') #.to('cpu')
#audio_path=input("audio_path:")
#audio_path=audio_path.strip("'")
# 指定音频文件路径
# audio_path = '\'/Users/cps/Documents/00-RESEARCH_copy/00-Praat_TestingStation/01-Scripts/speech_tools/whisper_s2t/SOODO1073582871_20241226.mp3\''
# print(audio_path)
# 进行语音识别，并指定语言为中文（zh）
#result = model.transcribe(audio_path,language='zh')
#print(result["text"])


import argparse
import os
try:
    import whisper
    from pydub import AudioSegment
except ValueError:
    print("modules request not installed please run 'pip3 install whisper pydub'.")

debug_output=False
# 指定输出文件夹和文件名
# output_folder = input('save folder: ')  # 目标文件夹
# output_filename = audio_path.rstrip('.mp3')  # 目标文件名
# output_path = output_filename+'.srt'

# 确保输出文件夹存在
# os.makedirs(output_folder, exist_ok=True)

# 进行语音识别，输出格字幕数据
# result = model.transcribe(audio_path, language="zh", initial_prompt="大型贪污，明年重点打击。")
# result = model.transcribe(audio_path, language="zh", initial_prompt="大型贪污，明年重点打击。",word_timestamps=True)




# 生成 SRT 字幕内容(句子)
# srt_content = ""
# for i, segment in enumerate(result["segments"], start=1):
#     start_time = format_timestamp(segment["start"])
#     end_time = format_timestamp(segment["end"])
#     text = segment["text"].strip()
#     srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"



# 生成 SRT 字幕内容(词)
# srt_content = ""
# j=1
# for i, segment in enumerate(result["segments"], start=1):
#     for word in segment["words"]:
#         # print(f"单词: {word['word']}, 开始时间: {word['start']}, 结束时间: {word['end']}")
#         start_time = format_timestamp(word["start"])
#         end_time = format_timestamp(word["end"])
#         text = word["word"].strip()
#         srt_content += f"{j}\n{start_time} --> {end_time}\n{text}\n\n"
#         j+=1
    # print(segment)

# 保存 SRT 文件
# with open(output_path, "w", encoding="utf-8") as f:
#     f.write(srt_content)
# print(f"字幕已保存到 {output_path}")

def validate(args):
    global debug_output
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
    if not os.path.isdir(args.source_path):
            if not args.source_path.endswith(".mp3"):
                print("Error: Source path is not a folder or file.")
                return False
    if args.debug:   
        debug_output=True
    return True    

def main(args):
    """
    Main function for the command-line interface.
    """
    #process command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help="Path to the mp3 file or path to mp3 file's folder",nargs='?')
    parser.add_argument('-d', '--debug',help="Debug mode will out put debug messages",action='store_true')      
    args = parser.parse_args()
    if not validate(args):
        return 1

    audio_path = args.source_path
    audio_path = audio_path.strip("'")

    
    if os.path.isdir(audio_path):
        for filename in os.listdir(audio_path):
            if filename.endswith(".mp3"):
                mp3_path = os.path.join(audio_path, filename)
                srt_file=convert_mp3_to_srt(mp3_path)
        exit(0)
    else:
        # 进行语音识别，输出格字幕数据
        srt_file=convert_mp3_to_srt(audio_path)
        exit(0)

def convert_mp3_to_srt(file):
    """
    Converts an MP3 audio file to an SRT subtitle file using the Whisper model.

    Parameters:
    file (str): The path to the MP3 audio file to be converted.

    The function performs the following steps:
    1. Loads the Whisper model.
    2. Transcribes the audio file to obtain subtitle data.
    3. Formats the transcription results into SRT subtitle format.
    4. Generates the output SRT file name based on the input file name.
    5. Saves the SRT content to the output file.

    The function prints a message indicating the location of the saved SRT file.
    """
    if debug_output:
        print(f"Converting MP3 file to SRT: {file}")
        print(f"{file} length: {get_audio_duration(file)} ms")
    # 加载 Whisper 模型
    model = whisper.load_model("large")
    # 进行语音识别，输出格字幕数据
    result = model.transcribe(file, language="zh", initial_prompt="大型贪污，明年重点打击。")
    if debug_output:
        print(result)
        print("-------------------------------------------")
    # 生成 SRT 字幕内容
    srt_content = ""
    for i, segment in enumerate(result["segments"], start=1):
        if debug_output:
            print(segment)
        start_time = format_timestamp(segment["start"])
        if i < len(result["segments"]):
            end_time = format_timestamp(result["segments"][i]["start"])
        else:
            end_time = get_file_end_timestamp(file)
        text = segment["text"].strip()
        srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
    # 生成 SRT 文件名
    output_path=os.path.splitext(file)[0]+".srt"
    # 保存 SRT 文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"将音频文件{file}转换为字幕文件{output_path}")
    return output_path       


def format_timestamp(seconds):
    millisec = int((seconds % 1) * 1000)
    time_str = f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02},{millisec:03}"
    return time_str

def get_audio_duration(file):
    audio = AudioSegment.from_file(file)
    result = len(audio)/1000
    if debug_output:
        print(f"Duration of audio file: {result} ms")
    return result

def get_file_end_timestamp(file):
    end_time = get_audio_duration(file)
    time_str = format_timestamp(end_time)
    if debug_output:
        print(f"End time of audio file: {time_str}")
    return time_str


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))