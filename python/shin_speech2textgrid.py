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

import whisper
import os
from shin_speech2srt import convert_mp3_to_srt
from shin_srt2textgrid import covert_srt_to_textgrid
# from praatio import textgrid as tgio
# from datetime import datetime
# from srt import parse




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

def main(args):
    audio_path = input('audio filename:')    #请替换为你的音频文件路径
    audio_path = audio_path.strip("'")
    if not os.path.exists(audio_path):
        print("Error: Source path is not a folder or file.")
        exit(1)
    if os.path.isdir(audio_path):
        # 遍历源目录中的文件
        for filename in os.listdir(audio_path):
            if filename.endswith(".mp3"):
                mp3_path = os.path.join(audio_path, filename)
                # 进行语音识别，输出格字幕数据
                srt_file=convert_mp3_to_srt(mp3_path)
                print(f"已将 {mp3_path} 转换为 {srt_file}")
                textgrid_file=covert_srt_to_textgrid(srt_file)
                print(f"已将 {srt_file} 转换为 {textgrid_file}")
        exit(0)
    else:
        if not audio_path.endswith(".mp3"):
            print("Error: Source file is not a mp3 file.")
            exit(1)
        # 进行语音识别，输出格字幕数据
        srt_file=convert_mp3_to_srt(audio_path)
        print(f"已将 {audio_path} 转换为 {srt_file}")
        textgrid_file=covert_srt_to_textgrid(srt_file)
        print(f"已将 {srt_file} 转换为 {textgrid_file}")
        exit(0)
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))