import os
import argparse
import shin_speech2srt as s2s
import re
debug_output=False
def validate(args):
    global debug_output
    if not args.source_path:
        print("Error: You need to specify a source path.")
        return False
    else:
        if not os.path.exists(args.source_path):
            print("Error: Source path is not a folder or file.")
            return False
    if not args.audio_path:
        args.audio_path=args.source_path
    else:
        if not os.path.exists(args.audio_path):
            print("Error: audio path is not a folder or file.")
            return False
        
    if os.path.isdir(args.source_path)!=os.path.isdir(args.audio_path):
        print("Error: Source path and audio path must be both folder or file.")
        return False
    if os.path.isfile(args.source_path):
        if not args.source_path.endswith(".srt"):
            print("Error: Source file is not a srt file")
            return False
    if os.path.isfile(args.audio_path):
        if not args.audio_path.endswith(".mp3"):
            print("Error: Audio file is not a mp3 file")
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
    parser.add_argument('source_path', help="Path to the srt file or path to srt file's folder",nargs='?')
    parser.add_argument('audio_path', help="Path to the mp3 file",nargs='?')  
    parser.add_argument('-d', '--debug',help="Debug mode will out put debug messages",action='store_true')      
    args = parser.parse_args()
    if not validate(args):
        return 1

    srt_path = args.source_path
    srt_path = srt_path.strip("'")
    audio_path = args.audio_path    
    audio_path = audio_path.strip("'")
   
    if os.path.isdir(srt_path):
        for filename in os.listdir(srt_path):
            if filename.endswith(".srt"):
                filename_no_ext = os.path.splitext(filename)[0]
                srt_file = os.path.join(srt_path, filename)
                mp3_file=  os.path.join(audio_path, filename_no_ext+".mp3")
                fix_srt_endtime(srt_file,mp3_file)
                print(f"已将 {srt_file} 结尾时间修正")
        exit(0)
    else:
        # 进行语音识别，输出格字幕数据
        srt_file=srt_path
        mp3_file= audio_path
        srt_file=fix_srt_endtime(srt_file,mp3_file)
        exit(0)

def fix_srt_endtime(srt_file,mp3_file):
    if not os.path.exists(mp3_file):
        print(f"Error: {mp3_file} not found.")
        exit(1)
    correct_end_time =s2s.get_file_end_timestamp(mp3_file)
    if debug_output:
        print(f"Correct end time is {correct_end_time}")

    with open(srt_file, "r", encoding="utf-8") as file:
        content = file.read().strip()
    matches = re.findall(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", content)
    if not matches:
        print("未找到任何字幕时间戳")
        return

    # 获取最后一组时间戳
    last_start_time, last_end_time = matches[-1]
    new_content = re.sub(
        re.escape(f"{last_start_time} --> {last_end_time}"),
        f"{last_start_time} --> {correct_end_time}",
        content
    )
    with open(srt_file, "w", encoding="utf-8") as file:
        file.write(new_content)

    print(f"已更新最后的时间戳：{last_end_time} -> {correct_end_time}")

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))    
# End of patch_fix_srt_endtime.py   