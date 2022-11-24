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

#frame to video 변환
def fraTovi(frame_dir, result_name, fps): # frame_dir : 비디오로 변환할 프레임이 있는 디렉토리 이름
                                          # 변환 결과 비디오 이름 지정
                                          # fps 지정
    clips = []

    directory = sorted(os.listdir('./frame/'+frame_dir))
    print(directory)

    for filename in directory:
        if filename.endswith(".jpg"):
            clips.append(ImageClip("./frame/" + frame_dir + "/" + filename).set_duration(1/fps))
    print(clips)

    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(result_name + '.mp4', fps=fps)

if __name__ == "__main__":
    #clip("Clouds", 0, 10, "clip")
    #frame("clip", 6)
    fraTovi("clip", "result", 6)
