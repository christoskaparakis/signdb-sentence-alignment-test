import ffmpeg  # install 'ffmpeg-python'
import os
###
import pysubs2
from pysubs2 import time
from datetime import datetime


###


def get_path_out(counter_file, counter_seg):
    # create a new directory (if it doesn't exist yet) and return path
    ROOT_DIR = os.path.abspath(os.curdir)
    new_dir = '/video segments'
    path = ROOT_DIR + new_dir
    try:
        os.mkdir(path)
    except OSError:
        pass
    return os.path.join(path, 'video{}segment{}.mp4'.format(counter_file, counter_seg))


counter_files = 0
for file in os.listdir('videos and timestamp seg'):
    if file.endswith('.ts'):
        counter_files += 1
        f = open('videos and timestamp seg/segments{}.txt'.format(counter_files))
        counter_segments = 1

        ###
        # code for subtitles segments
        subs = pysubs2.load("videos and timestamp seg/subs-test-video{}.txt".format(counter_files), encoding="utf-8") # change subs location
        ####

        next(f)  # skip first line of timestamps file
        for line in f:
            timestamps = line.replace('\t', ' ').split(' ')
            start = timestamps[0]
            print(start)
            end = timestamps[1]
            # stream = ffmpeg.input('videos and timestamp seg/video{}.ts'.format(counter_files))
            # stream = ffmpeg.trim(stream, start=start, end=end)  # start_pts, end_pts to use timestamps
            # stream = ffmpeg.output(stream, get_path_out(counter_files, counter_segments))
            # ffmpeg.run(stream)


            ###
            alignedsub = ''

            startms = pysubs2.time.timestamp_to_ms(time.TIMESTAMP.match(start).groups())  # start time of segment in ms
            endms = pysubs2.time.timestamp_to_ms(time.TIMESTAMP.match(end).groups())  # end time of segment in ms

            i = 0
            for l in subs:
                # print(l.start)  # shows the start timestamp in miliseconds
                # print(l.end)
                if i > 1 and l.start < endms:  # first 2 subs are the same in every file (date etc)
                    if l.start < startms < l.end:
                        # if subtitle starts before the video segment starts and ends while the video segment still
                        # plays
                        if ('.' in l.text) or ('?' in l.text):
                            if '.' in l.text:
                                if subs[i].text.split('.')[1] != '':
                                    alignedsub += ' ' + subs[i].text.split('.')[1]
                                else:
                                    alignedsub += ' ' + subs[i].text
                            elif '?' in l.text:
                                if subs[i].text.split('?')[1] != '':
                                    alignedsub += ' ' + subs[i].text.split('?')[1]
                                else:
                                    alignedsub += ' ' + subs[i].text

                        elif ('.' in subs[i - 1].text) or ('?' in subs[i - 1].text):
                            if '.' in subs[i - 1].text:
                                if subs[i-1].text.split('.')[1] != '':
                                    alignedsub += ' ' + subs[i - 1].text.split('.')[1]
                                else:
                                    alignedsub += ' ' + subs[i].text
                            elif '?' in subs[i - 1].text:
                                if subs[i - 1].text.split('?')[1] != '':
                                    alignedsub += ' ' + subs[i - 1].text.split('?')[1]
                                else:
                                    alignedsub += ' ' + subs[i].text

                        else:
                            alignedsub += ' ' + subs[i].text

                    elif l.start > startms and l.end < endms:
                        # if subtitle starts and ends while the video segment is playing
                        alignedsub += ' ' + subs[i].text

                    elif l.start < endms < l.end:
                        # if subtitle starts before the video segment ends and continues after that
                        if ('.' in l.text) or ('?' in l.text):
                            if '.' in l.text:
                                alignedsub += ' ' + subs[i].text.split('.')[1]
                            elif '?' in l.text:
                                alignedsub += ' ' + subs[i].text.split('?')[1]
                        elif ('.' in subs[i - 1].text) or ('?' in subs[i - 1].text):
                            if '.' in subs[i - 1].text:
                                alignedsub = alignedsub.replace(alignedsub.split('.')[-1], '')
                            elif '?' in subs[i - 1].text:
                                alignedsub = alignedsub.replace(alignedsub.split('?')[-1], '')
                i += 1
            alignedsub = alignedsub.replace("\\N", " ")
            print(alignedsub)
            text_file = open('subtitle segments/subsegment{}.txt'.format(counter_segments), "w")
            text_file.write(alignedsub)
            text_file.close()
            ###
            counter_segments += 1
print('segments created for ', counter_files, ' video.')
