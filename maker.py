# -*- coding: utf-8 -*-
from turtle import width
import librosa
import glob
import math
import os
import random

# 作用：将一张图制作为视频。背景音是MP3，视频将是mp3长度。
# 用法：将要转换的mp3和视频要用的封面图放在本文件夹下。启动maker.py。

width=480
height=272
FPS=25


music=glob.glob("*.mp3")
pics=glob.glob("*.png")+glob.glob("*.jpg")

print("正在自动清理mp4文件")
movies=glob.glob("*.mp4")
for movie in movies:
    os.remove(movie) 

for i in music:
    use_pic=random.choice(pics)
    #获取音频时长
    duration = math.ceil(librosa.get_duration(filename=i))
    print(f"开始为- {i} -生成图片视频...")
    #生成和音频一个上传的视频
    os.system(f"ffmpeg -r {FPS} -loop 1 -i {use_pic} -pix_fmt yuv420p -vcodec libx264 -b:v 1600k \
         -r:v 25 -preset medium -crf 30 -s {width}x{height} -vframes 250 -r 25 -t {duration} out.mp4  -hwaccel \
             nvdec -hwaccel_output_format cuda")
    print(f"- {i} -图片视频生成完毕...")
    os.system(f'ffmpeg -i out.mp4 -i "{i}" -c:v copy -c:a aac -strict experimental "{i.replace(".mp3","")}.mp4" \
        -hwaccel nvdec -hwaccel_output_format cuda')
    print(f"- {i} -视频拼合完毕...")
    os.remove("out.mp4")
    print(f"- {i}.mp4 -视频制作完毕...")
print("所有视频已制作完毕。")

