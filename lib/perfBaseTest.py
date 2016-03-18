__author__ = 'shako'
import unittest
from selenium import webdriver
from videoUtilHelper import RecordingVideoObj
from videoUtilHelper import VideoAnalyzeObj
from selenium.webdriver.common.keys import Keys
import time
import io
import os

DEFAULT_THIRDPARTY_DIR = os.path.join(os.getcwd(), "thirdParty")
DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), "output")
DEFAULT_VIDEO_OUTPUT_DIR = os.path.join(DEFAULT_OUTPUT_DIR, "videos")
DEFAULT_PROFILE_OUTPUT_DIR = os.path.join(DEFAULT_OUTPUT_DIR, "profiles")
DEFAULT_IMAGE_OUTPUT_DIR = os.path.join(DEFAULT_OUTPUT_DIR, "images", "output")
DEFAULT_IMAGE_SAMPLE_DIR = os.path.join(DEFAULT_OUTPUT_DIR, "images", "sample")

DEFAULT_GECKO_PROFILER_PATH = os.path.join(DEFAULT_THIRDPARTY_DIR, "geckoprofiler-signed.xpi")

DEFAULT_BROWSER_POS_X = 0
DEFAULT_BROWSER_POS_Y = 0
DEFAULT_BROWSER_WIDTH = 1200
DEFAULT_BROWSER_HEIGHT = 980


class PerfBaseTest(unittest.TestCase):

    video_recording_obj = None
    driver = None

    def setUp(self):

        # TODO: ask if user wants to overwrite the profiler recordings and video
        # Install gecko profiler addon
        # Ref: https://github.com/bgirard/Gecko-Profiler-Addon
        fp = webdriver.FirefoxProfile()
        fp.add_extension(extension=DEFAULT_GECKO_PROFILER_PATH)

        # Start video recording
        self.output_name = self.__class__.__name__ + "_" + str(int(time.time()))
        self.video_output_fp = os.path.join(DEFAULT_VIDEO_OUTPUT_DIR, self.output_name + ".mkv")
        self.video_output_sample_1_fp = os.path.join(DEFAULT_VIDEO_OUTPUT_DIR, self.output_name + "_sample_1.mkv")
        self.video_output_sample_2_fp = os.path.join(DEFAULT_VIDEO_OUTPUT_DIR, self.output_name + "_sample_2.mkv")
        self.img_sample_dp = os.path.join(DEFAULT_IMAGE_SAMPLE_DIR, self.output_name)
        # TODO: Extract the framerate as a variable?
        self.video_recording_obj = RecordingVideoObj()
        self.video_recording_obj.start_video_recording(self.video_output_fp)

        # The profiler starts automatically
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.set_window_position(DEFAULT_BROWSER_POS_X, DEFAULT_BROWSER_POS_Y)
        self.driver.set_window_size(DEFAULT_BROWSER_WIDTH, DEFAULT_BROWSER_HEIGHT)

    def tearDown(self):
        # Stop gecko profiler recording
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + '2')
        # Stop video recording
        self.video_recording_obj.stop_video_recording()
        time.sleep(10) #XXX: Change this to active wait

        # Switch to the cleopetra.io tab
        main_window = self.driver.current_window_handle
        self.driver.switch_to_window(main_window) # Switch to current frame

        self.driver.set_script_timeout(5)
        recording = self.driver.execute_async_script(
            "var done = arguments[0];" +
            "console.log(done);" +
            "window.Parser.getSerializedProfile(true, function (serializedProfile) {" +
            "  done(serializedProfile);"
            "});"
        )

        # TODO: Name the profile with timestamp
        with io.open(os.path.join(DEFAULT_PROFILE_OUTPUT_DIR, self.output_name + ".bin"), 'w', encoding='utf-8') as f:
            f.write(recording)
        self.driver.close()

        video_analyze_obj = VideoAnalyzeObj()
        img_output_dp = os.path.join(DEFAULT_IMAGE_OUTPUT_DIR, self.output_name)
        os.mkdir(img_output_dp)

        video_analyze_obj.run_analyze(self.video_output_fp, img_output_dp, self.img_sample_dp)


