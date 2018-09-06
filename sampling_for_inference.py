from os import listdir
from os.path import join, isfile
import cv2
from dataset.utils.shared import dir_test, dir_originals
import random

video_length = 200
sample_size = 100

def save_sliced_video(input_file, output_file):
    try:
        video = cv2.VideoCapture(input_file)
        count = 0
        frames = []
        frames_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        start_frame = 1
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        while count < video_length:
            ret, frame = video.read()
            if not ret:
                break
            frames.append(frame)
            count += 1
        fps = video.get(cv2.CAP_PROP_FPS)
        size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, fourcc, fps, size)
        # check if video has required length if not return false
        # assert len(frames) == frames_per_video
        for f in frames:
            out.write(f)
        video.release()
        out.release()
        return True
    except:
        return False


def slice_all():
    # iterate over each file in the source directory
    file_list = listdir(dir_originals)
    print("Start sampling %d files" % len(file_list))
    count = 0
    for j in range(sample_size):
        r = random.randint(0,len(file_list)-1)
        file_name = file_list[r]
        input_file = join(dir_originals, file_name)
        new_file_name = "video_" + format(count, '05d') + ".avi"
        output_file = join(dir_test, new_file_name)
        if isfile(input_file):
            flag = save_sliced_video(input_file, output_file)
            if flag:
                count += 1
        if count % 10 == 0:
            print("Processed %d out of %d" % (count, len(file_list)))
    print("Sampling completed %d out of %d" % (count, len(file_list)))

slice_all()
