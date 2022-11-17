# Genshin-Vision-Videos
用于神之眼挂件的视频文件。

Video files for electronic vision pendant.

项目中的视频来源于以下项目，通过GPL3.0协议授权：

The videos in the project are from the following projects, licensed under GPL 3.0:

- [神之眼挂件V1.2_ESP32U](https://oshwhub.com/Myzhazha/shen-zhi-yan-gua-jian-v1-2_esp32u)
- [璃月神之眼挂件](https://oshwhub.com/Myzhazha/li-yue-shen-zhi-yan-gua-jian)

## 中文
### 我该如何选用合适的视频？
项目中的文件夹名称含义如下所示，请依据分辨率、屏幕形状（视频旋转角度）进行选择：
```
帧宽度_帧高度_屏幕形状_旋转角度
```
其中，`Round`为圆形屏幕，`Square`为方形屏幕

### 如何转换已有的mp4视频文件至mjpeg？
首先准备好分辨率合适的视频，随后在命令行中输入以下命令进行转换：
```
python convert2MJPEG.py "包含视频的文件夹路径"
```

### 脚本在转换中做了什么？
`convert2MJPEG.py`会将普通RGB888格式mp4视频转换为MJPEG格式，在将色域缩减至RGB565的同时使用抖动算法以保证观感。

## English
### How do I choose appropriate videos?
The meaning of the folder name of this project is as follows, you can choose by resolution and screen shape (video rotation angle):
```
Width_Height_Screen shapre_Rotation angle
```

### How to convert existing video file in mp4?
Prepare video with appropriate resolution, then use following command in command line to convert:
```
python convert2MJPEG.py "path to folder which contains videos"
```

### What does the script do?
`convert2MJPEG.py` converts ordinary RGB888 format mp4 video to MJPEG, using jitter algorithm to ensure experience while reducingcolor gamut to RGB565.
