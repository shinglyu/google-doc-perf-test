__author__ = 'shako'
import os
import cv2
import time
import argparse
import numpy as np
from argparse import ArgumentDefaultsHelpFormatter

DEFAULT_IMG_DIR_PATH = os.path.join(os.getcwd(), "images")
DEFAULT_SAMPLE_DIR_PATH = os.path.join(os.getcwd(), "sample")

class VideoAnalyzer(object):

    def __init__(self, input_video_fp):
        self.video_fp = input_video_fp
        self.image_list = []

    def convert_video_to_images(self):
        vidcap = cv2.VideoCapture(self.video_fp)
        result, image = vidcap.read()
        img_cnt = 1
        while result:
            str_image_fp = os.path.join(DEFAULT_IMG_DIR_PATH, "image_%d.jpg" % img_cnt)
            cv2.imwrite(str_image_fp, image)
            result, image = vidcap.read()
            img_cnt += 1
            self.image_list.append({"time_seq": vidcap.get(0), "image_fp": str_image_fp})

        return self.image_list

    def compare_with_sample_image(self):
        result_list = []
        print "Comparing sample file start %s" % time.strftime("%c")
        sample_fn_list = os.listdir(DEFAULT_SAMPLE_DIR_PATH)
        sample_fn_list.sort()
        search_index = 0
        for sample_fn in sample_fn_list:
            sample_fp = os.path.join(DEFAULT_SAMPLE_DIR_PATH, sample_fn)
            sample_dct = self.convert_to_dct(sample_fp)
            for img_index in range(search_index, len(self.image_list)):
                image_data = self.image_list[img_index]
                comparing_dct = self.convert_to_dct(image_data['image_fp'])
                print "Comparing  sample file [%s] with imgae file [%s]" % (sample_fn, image_data['image_fp'])
                #if self.compare_two_images(sample_dct, comparing_dct):
                if self.compare_two_images(sample_fp, image_data['image_fp']):
                    print "Comparing sample file end %s" % time.strftime("%c")
                    result_list.append(image_data)
                    search_index = img_index + 1
                    if len(result_list) == len(os.listdir(DEFAULT_SAMPLE_DIR_PATH)):
                        return result_list
                    break
        print "Comparing sample file end %s" % time.strftime("%c")
        return result_list

    def convert_to_dct(self, image_fp):
        img_obj = cv2.imread(image_fp)
        imgcv = cv2.split(img_obj)[0]
        imf = np.float32(imgcv) / 255.0
        dct_obj = cv2.dct(imf)
        return dct_obj

    #def compare_two_images(self, dct_obj_1, dct_obj_2):
    #    match = False
    #    row1, cols1 = dct_obj_1.shape
    #    row2, cols2 = dct_obj_2.shape
    #    if (row1 != row2) or (cols1 != cols2):
    #        match = False
    #    else:
    #        mismatch = 0
    #        for i in range(1, row1):
    #            for j in range(1, cols1):
    #                px1 = dct_obj_1[i, j]
    #                px2 = dct_obj_2[i, j]
    #                if abs((px1 - px2) / px1) > 0.05:
    #                    print px1
    #                    print px2
    #                    print abs((px1 - px2) / px1)
    #                    mismatch += 1
    #                    return match
    #        if mismatch == 0:
    #            match = True
    #    return match

    def compare_two_images(self, image1_fp, image2_fp):
        match=False
        img1 = cv2.imread(image1_fp)
        img2 = cv2.imread(image2_fp)
        row1, cols1, channel1 = img1.shape
        row2, cols2, channel2 = img2.shape
        if (row1 != row2) or (cols1 != cols2) or (channel1 != channel2):
            match=False
            return match
        else:
            mismatch = 0
            for i in range(1, row1):
                for j in range(1, cols1):
                    px1 = img1[i, j]
                    px2 = img2[i, j]
                    if (abs(px1[0] - px2[0]) > 5 or abs(px1[1] - px2[1]) > 5 or abs(px1[2] - px2[2]) > 5):
                        mismatch += 1
                        return match
            if(mismatch==0):
                match=True
            else:
                match=False
            return match

    def run(self):
        pass


def main():
    arg_parser = argparse.ArgumentParser(description='Performance Video Analyzer',
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    arg_parser.add_argument('-i', '--input', action='store', dest='input_video_fp', default=None,
                            help='Specify the video file path.', required=True)
    args = arg_parser.parse_args()
    input_fp = args.input_video_fp
    run_obj = VideoAnalyzer(input_fp)
    run_obj.convert_video_to_images()
    #run_obj.image_list.append({"time_seq": 10, "image_fp": "images/image_541.jpg"})
    print run_obj.compare_with_sample_image()

if __name__ == '__main__':
    main()
