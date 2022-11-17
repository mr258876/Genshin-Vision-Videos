from concurrent import futures
from itertools import repeat
import os
import sys
import cv2

# Dither Tresshold for Red Channel
dither_tresshold_r = [
    1, 7, 3, 5, 0, 8, 2, 6,
    7, 1, 5, 3, 8, 0, 6, 2,
    3, 5, 0, 8, 2, 6, 1, 7,
    5, 3, 8, 0, 6, 2, 7, 1,
    0, 8, 2, 6, 1, 7, 3, 5,
    8, 0, 6, 2, 7, 1, 5, 3,
    2, 6, 1, 7, 3, 5, 0, 8,
    6, 2, 7, 1, 5, 3, 8, 0
]

# Dither Tresshold for Green Channel
dither_tresshold_g = [
    1, 3, 2, 2, 3, 1, 2, 2,
    2, 2, 0, 4, 2, 2, 4, 0,
    3, 1, 2, 2, 1, 3, 2, 2,
    2, 2, 4, 0, 2, 2, 0, 4,
    1, 3, 2, 2, 3, 1, 2, 2,
    2, 2, 0, 4, 2, 2, 4, 0,
    3, 1, 2, 2, 1, 3, 2, 2,
    2, 2, 4, 0, 2, 2, 0, 4
]

# Dither Tresshold for Blue Channel
dither_tresshold_b = [
    5, 3, 8, 0, 6, 2, 7, 1,
    3, 5, 0, 8, 2, 6, 1, 7,
    8, 0, 6, 2, 7, 1, 5, 3,
    0, 8, 2, 6, 1, 7, 3, 5,
    6, 2, 7, 1, 5, 3, 8, 0,
    2, 6, 1, 7, 3, 5, 0, 8,
    7, 1, 5, 3, 8, 0, 6, 2,
    1, 7, 3, 5, 0, 8, 2, 6
]

# Get 16bit closest color
def closest_rb(c):
    return (c >> 3 << 3) # red & blue
def closest_g(c):
    return (c >> 2 << 2) # green

# RGB565
def RGB16BIT(r, g, b):
    return (((r>>3)<<11)|((g>>2)<<5)|(b>>3))

# Dithering by individual subpixel
def dither_xy(x: int, y: int, r, g, b):
    # Get Tresshold Index
    tresshold_id = ((y & 7) << 3) + (x & 7)

    r = closest_rb(
          min(r + dither_tresshold_r[tresshold_id], 0xff))
    g = closest_g(
          min(g + dither_tresshold_g[tresshold_id], 0xff))
    b = closest_rb(
          min(b + dither_tresshold_b[tresshold_id], 0xff))

    # return RGB16BIT(r, g, b)
    return r, g, b

# Convert
def convert(src):
    vRead = cv2.VideoCapture(src)
    vW = int(vRead.get(cv2.CAP_PROP_FRAME_WIDTH))
    vH = int(vRead.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vFPS = int(vRead.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc("M","J","P","G")
    vWrite = cv2.VideoWriter(src.replace(".mp4", ".mjpeg"), fourcc, vFPS, (vW, vH))

    # fourcc = cv2.VideoWriter_fourcc("M","P","4","V")
    # vWrite = cv2.VideoWriter(src.replace(".mjpeg", "RGB565.mp4"), fourcc, vFPS, (vW, vH))

    executor = futures.ProcessPoolExecutor(os.cpu_count())
    frameList = []

    while(True):
        ret, frame = vRead.read()
        if ret:
            frameList.append(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    resultList = executor.map(convertFrame, frameList, repeat(vW), repeat(vH))
    for f in resultList:
        vWrite.write(f)

    vWrite.release()
    vRead.release()

def convertFrame(frame, width, height):
    for y in range(height):
            for x in range(width):
                r, g, b = dither_xy(x, y, frame[x][y][0], frame[x][y][1], frame[x][y][2])
                frame[x][y][0] = r
                frame[x][y][1] = g
                frame[x][y][2] = b
    return frame

def main():
    p = ""
    if len(sys.argv) > 1:
        p = sys.argv[1]
    else:
        print("Missing argument: folder with video file to convert")

    fileList = os.listdir(p)
    for f in fileList:
        fp = p +"/"+f
        print("Now Processing: %s" % fp)
        if os.path.isfile(fp) and fp.endswith(".mp4"):
            convert(fp)

if __name__ == "__main__":
    main()