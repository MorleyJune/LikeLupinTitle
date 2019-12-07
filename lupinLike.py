#!/usr/bin/env python3
# coding: utf-8

import os
import io
import sys
import re
import codecs
from binascii import hexlify

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='shift_jis')
f = open( "lupin.exo", "w")
if len(sys.argv) <= 1:
    print("Usage: lupin3rdtwexo.py [-g] <string to type> <sound file (in full path)>")
    sys.exit(1)

is_grouping = 0
if sys.argv[1] == '-g':
    is_grouping = 1
    args = sys.argv[1:]
else:
    args = sys.argv


tmpstr = args[1]
if len(args) == 3:
    soundfile1 = args[2]
else:
    soundfile1 = os.getcwd() + "\\typewriter-1.mp3"

if len(args) == 4:
    soundfile2 = args[3]
else:
    soundfile2 = os.getcwd() + "\\lupin.wav"


# 最後の音の長さ
soundLen = 231

# 入力された文字列のうち、文字列のスペースは削除
inputstr = re.sub(r'\s+',"",tmpstr)
noLineInputStr = re.sub(r'\\n+', "", inputstr)
noLineStrLen = len( noLineInputStr )
if noLineStrLen % 2 == 0:
    frameNum = noLineStrLen // 2 * 25
else :
    frameNum = noLineStrLen // 2 * 25 + 13

# ヘッダの文字列を出力する。
f.write('[exedit]\n')
f.write('width=1280\n')
f.write('height=720\n')
f.write('rate=60\n')
f.write('scale=1\n')
f.write( 'length={0:d}'.format(frameNum + soundLen) )
f.write("\n")
f.write('audio_rate=44100\n')
f.write('audio_ch=2\n')


# ルパンタイトル文字列, 金の髭氏のスクリプトを使用
f.write('[0]\n')
f.write('start=1\n')
f.write('end={0:d}\n'.format( frameNum + soundLen ) )
f.write('layer=1\n')
f.write('overlay=1\n')
f.write('camera=0\n')
if is_grouping == 1:
    f.write('group=1\n')
f.write('[0.0]\n')
f.write('_name=テキスト\n')
f.write('サイズ=300\n')
f.write('表示速度=0.0\n')
f.write('文字毎に個別オブジェクト=1\n')
f.write('移動座標上に表示する=0\n')
f.write('自動スクロール=0\n')
f.write('B=0\n')
f.write('I=0\n')
f.write('type=0\n')
f.write('autoadjust=0\n')
f.write('soft=1\n')
f.write('monospace=0\n')
f.write('align=4\n')
f.write('spacing_x=0\n')
f.write('spacing_y=0\n')
f.write('precision=1\n')
f.write('color=ffffff\n')
f.write('color2=000000\n')
f.write('font=幻ノにじみ明朝\n')
ii = hexlify(inputstr.encode('utf-16'))
hex_str = ii.decode('ascii')
hex_str = hex_str.lstrip("fffe").replace("5c006e00", "0d000a00")
f.write("text=" + hex_str)
for x in range(len(hex_str),4096,4):
    f.write("0000")
f.write("\n")

f.write("[0.1]\n")
f.write("_name=アニメーション効果\n")
f.write("track0=20.00\n")
f.write("track1=10.00\n")
f.write("track2=100.00\n")
f.write("track3=20.00\n")
f.write("check0=0\n")
f.write("type=0\n")
f.write("filter=0\n")
f.write("name=ルパン\n")
f.write("param=\n")

f.write("[0.2]\n")
f.write("_name=アニメーション効果\n")
f.write("track0=250.00\n")
f.write("track1=0.00\n")
f.write("track2=0.00\n")
f.write("track3=0.00\n")
f.write("check0=0\n")
f.write("type=3\n")
f.write("filter=0\n")
f.write("name=\n")
f.write("param=\n")

f.write("[0.3]\n")
f.write("_name=発光\n")
f.write("強さ=114.6\n")
f.write("拡散=250\n")
f.write("しきい値=80.0\n")
f.write("拡散速度=0\n")
f.write("サイズ固定=0\n")
f.write("color=ffffff\n")
f.write("no_color=1\n")

f.write("[0.4]\n")
f.write("_name=標準描画\n")
f.write("X=0.0\n")
f.write("Y=0.0\n")
f.write("Z=0.0\n")
f.write("拡大率=250.00\n")
f.write("透明度=0.0\n")
f.write("回転=0.00\n")
f.write("blend=0\n")

# ここから音声ファイル,タイプライター音

if soundfile1 == '':
   sys.exit(0)     

sl = len(noLineInputStr)
pos = 1
start = 1
end = 12
for i in range(0,sl):
    f.write('[{0:d}]\n'.format(pos))
    f.write('start={0:d}\n'.format(start))
    f.write('end={0:d}\n'.format(end))
    f.write('layer=2\n')
    f.write('overlay=1\n')
    f.write('audio=1\n')
    if is_grouping == 1:
        f.write('group=1\n')
    f.write('[{0:d}.0]\n'.format(pos))
    f.write('_name=音声ファイル\n')
    f.write('再生位置=0.00\n')
    f.write('再生速度=100.0\n')
    f.write('ループ再生=0\n')
    f.write('動画ファイルと連携=0\n')
    f.write('file='+soundfile1+'\n')
    f.write('[{0:d}.1]\n'.format(pos))
    f.write('_name=標準再生\n')
    f.write('音量=100.0\n')
    f.write('左右=0.0\n')
    start = end + 1
    if pos % 2 == 0:
        end += 12
    else:
        end += 13

    pos+=1

# 音声ファイル,最後の音

f.write("[{0:d}]".format(sl+1))
f.write("\n")
f.write("start={0:d}".format(start))
f.write("\n")
f.write("end={0:d}".format(start + soundLen ))
f.write("\n")
f.write("layer=2\n")
f.write("overlay=1\n")
f.write("audio=1\n")
f.write("[{0:d}.0]".format(sl+1))
f.write("\n")
f.write("_name=音声ファイル\n")
f.write("再生位置=0.00\n")
f.write("再生速度=100.0\n")
f.write("ループ再生=0\n")
f.write("動画ファイルと連携=0\n")
f.write('file='+soundfile2+'\n')
f.write("[{0:d}.1]".format(sl+1))
f.write("\n")
f.write("_name=標準再生\n")
f.write("音量=100.0\n")
f.write("左右=0.0\n")

# ファイルを閉じる
f.close()
