from moviepy.editor import *
import moviepy.video.fx.all as vfx
import os
import cv2

# 영상 구간 자르기 & crop
def clip(ori_name, start, end, clip_name):
    clip = VideoFileClip("./video/" + ori_name + ".mp4")
    clip = clip.without_audio()
    (w, h) = clip.size
    clip = vfx.crop(clip, width=100, height=100, x_center=w/2, y_center=h/2)
    clip = clip.subclip(start, end)
    clip.write_videofile("./video/" + clip_name + ".mp4")

# 영상 frame 분할
def frame(video_name, H_fps):
    video_path = "./video/" + video_name + ".mp4"
    directory_path = "./frame/" + video_name

    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    except OSError:
        print('Error: Creating directory. ' + directory_path)

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Could not Open :", video_path)
        exit(0)

    fps = round(video.get(cv2.CAP_PROP_FPS))
    HPS = round(fps / H_fps)

    count = 0
    number = 0

    while (True):

        ret, image = video.read()
        if not ret: break
        if (count % HPS == 0):
            #h, w, c = image.shape
            #mid_x, mid_y = w // 2, h // 2
            #image = image[mid_y - 50:mid_y + 50, mid_x - 50:mid_x + 50]
            cv2.imwrite("./frame/"+video_name+"/%06d.jpg" % number, image)
            print('Saved frame number :', str(int(video.get(1))))
            number += 1
        count += 1

    video.release()

if __name__ == "__main__":
    #clip("Clouds", 0, 10, "clip")
    frame("Clouds", 5)
