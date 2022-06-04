# -*- coding: utf-8 -*-
import librosa
import glob
import math
import os
import random
from PIL import Image

# 作用：将一张图制作为视频。背景音是MP3，视频将是mp3长度。
# 用法：将要转换的mp3和视频要用的封面图放在本文件夹下。启动maker.py。

width=1280
height=720
FPS=25
bg_color=(0,0,0)  #图片底色


music=glob.glob("*.mp3")
pics=glob.glob("*.jpg")

print("正在自动清理mp4文件")
movies=glob.glob("*.mp4")
for movie in movies:
    os.remove(movie) 

for i in music:
    use_pic=random.choice(pics)
    #获取音频时长
    duration = math.ceil(librosa.get_duration(filename=i))
    img=Image.open(use_pic)
    if img.height != height or img.width !=width:
        bg = Image.new('RGB', (width, height), bg_color)
        #跟着长边缩放。谁长，就按谁压
        if img.width>img.height:
            info=width/img.width
            img = img.resize((int(img.width*info), int(img.height*info)),Image.ANTIALIAS)
        else:
            info=height/img.height
            img = img.resize((int(img.width*info), int(img.height*info)),Image.ANTIALIAS)
        
        if img.width>img.height:
            bg.paste(img,(0,int((height-img.height)/2)))
        else:
            bg.paste(img,(int((width-img.width)/2),0))
        bg.save(f"{use_pic}")
        bg.close()
    img.close()
    print(f"开始为- {i} -生成图片视频...")
    #使用cuda完整视频制作
    os.system(f"ffmpeg -vsync 0 -hwaccel cuvid -c:v mjpeg_cuvid -framerate {FPS} -loop 1 -i {use_pic} -b:v 1600k -c:a copy -vf scale_cuda={width}:{height} -t {duration} -c:v h264_nvenc out.mp4")
    
    print(f"- {i} -图片视频生成完毕...")
    os.system(f'ffmpeg -i out.mp4 -i "{i}" -c:v copy -c:a aac -strict experimental "{i.replace(".mp3","")}.mp4" \
        -hwaccel nvdec -hwaccel_output_format cuda')
    print(f"- {i} -视频拼合完毕...")
    os.remove("out.mp4")
    print(f"- {i}.mp4 -视频制作完毕...")
print("所有视频已制作完毕。")

