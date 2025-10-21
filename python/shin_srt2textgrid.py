#This script is used to call Whisper model to execute speech-to-text task
#mainly transribing Chinese speech
#the transcription will be saved in srt format,
#and then transfer to textgrid format for phonetic analysis.
#This script will repeat the tasks above for all audio files and srt files in the same folder.
#created by dianqing82@gmail.com, 2025 (version 2025-03-05)
import argparse
import os
from datetime import datetime
try:
    from praatio import textgrid as tgio
    from srt import parse
except ValueError:
    print("modules request not installed please run 'pip3 install praatio srt'.")
    exit(1)
debug_output=False

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
            if not args.source_path.endswith(".srt"):
                print("Error: Source file is not a srt file")
                return False
    if args.debug:   
        debug_output=True
    return True    
def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', help="Path to the mp3 file or path to mp3 file's folder",nargs='?')
    parser.add_argument('-d', '--debug',help="Debug mode will out put debug messages",action='store_true')      
    args = parser.parse_args()
    if not validate(args):
        return 1
    audio_path =  args.source_path    #请替换为你的音频文件路径
    audio_path = audio_path.strip("'")
    if not os.path.exists(audio_path):
        print("Error: Source path is not a folder or file.")
        exit(1)
    if os.path.isdir(audio_path):
        # 遍历源目录中的文件
        for filename in os.listdir(audio_path):
            if filename.endswith(".srt"):
                srt_file = os.path.join(audio_path, filename)
                textgrid_file=covert_srt_to_textgrid(srt_file)
        exit(0)
    else:
        srt_file=audio_path
        textgrid_file=covert_srt_to_textgrid(srt_file)
        print(f"已将 {srt_file} 转换为 {textgrid_file}")
        exit(0)


def covert_srt_to_textgrid(srtFile):
    srtFileObj=open(srtFile)
    subs = parse(srtFileObj.read())
    entryList=[]
    tMax=0
    for sub in subs:
        startTime=sub.start.total_seconds()
        endTime=sub.end.total_seconds()
        label=sub.content
        intTier=(startTime,endTime,label)
        entryList.append(intTier)
        tMax=endTime
    srtFileObj.close()
    outputFile=os.path.splitext(srtFile)[0]+".TextGrid"
    print("Save TextGrid to {output} ".format(output=outputFile))
    tierName="s2t"
    if os.path.isfile(outputFile):
        tg = tgio.openTextgrid(outputFile,True)
        if tierName in tg.tierDict:
            tierName=tierName+datetime.now().strftime("%m%d%Y%H%M%S")
    else:
        tg = tgio.Textgrid()
    if debug_output:
        print("srtFile:",srtFile)
        print("entryList:",entryList)
    try:
        wordTier = tgio.IntervalTier(tierName, entryList, 0, tMax)
    except Exception as e:  
        print("Error: The srt file is not valid.")
        return None 
    tg.addTier(wordTier)
    tg.save(outputFile,'long_textgrid', True) 
    return outputFile


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))