# speech_tools

## Tools for speech analysis

## python/cc2shengyun.py

#### Convert Chinese characters to Hanyu Pinyin

### Installation

1. Install pypinyin
2. Run `pip3 install pypinyin`.

### Usage

```
$ python3 cc2shengyun.py 需要转换的汉字
$ xu1 yao4 zhuan3 huan4 de han4 zi4

```

## python/wav2srt.py
#### create srt file for wav files in a folder 
### Installation
1. Install autosub
2. Run `pip3 install autosub`.
### Usage
```
$ python3 wav2srt.py -h
$ python3 wav2srt.py --list-languages
$ python3 wav2srt.py path/to/wav/files/ -S zh-CN
```
## python/srt2textgrid.py
#### create textgrid tier from srt files
### Installation
1. Install praatio and srt
2. Run `pip3 install praatio srt`.
### Usage 
```
$ python3 srt2textgrid.py -h
$ python3 srt2textgrid.py path/to/srt/files/
$ python3 srt2textgrid.py path/to/file.srt
```

## python/wavsplit2textgrid.py
#### create textgrid tier from wav files split by pitch
### Installation
1. Install praatio and parselmouth
2. Run `pip3 install praat-parselmouth praatio`.
### Usage 
```
$ python3 wavsplit2textgrid.py -h
$ python3 wavsplit2textgrid.py path/to/wav/files/
$ python3 wavsplit2textgrid.py path/to/file.wav
```
### License

MIT
