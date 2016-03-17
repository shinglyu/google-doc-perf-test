import unittest
from selenium import webdriver
import json
import subprocess
from recordscreen import video_capture_line
from selenium.webdriver.common.keys import Keys
import time
import io
import os


class GoogleDocPerfTest(unittest.TestCase):
    _profile_name = "test"

    proc = None

    def setUp(self):
        self.docUrl = "https://docs.google.com/document/d/1HXDdOQuxQiX1bSrpAs4hJfTaim1iLO_xB01nokb0wT0/edit?usp=sharing"

        # TODO: ask if user wants to overwrite the profiler recordings and video

        # Install gecko profiler addon
        # Ref: https://github.com/bgirard/Gecko-Profiler-Addon
        fp = webdriver.FirefoxProfile()
        fp.add_extension(extension="geckoprofiler-signed.xpi")

        # Start video recording
        # TODO: Name the video with timestamp
        # TODO: Dynamically assign the screen resolution?
        # TODO: Extract the framerate as a variable?
        if os.path.exists("./tmp.mkv"):
            os.remove("./tmp.mkv")
        self.proc = subprocess.Popen(video_capture_line(90, 72, 125, 1280, 720, ":0.0", "h264", "./tmp.mkv"))

        # The profiler starts automatically
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1280, 820)
        self.driver.get(self.docUrl)

    def test_load(self):

        # Recording start marker
        self.driver.execute_script("var teststart = function(){document.getElementById('docs-branding-logo').style.backgroundColor = 'red'}; teststart()");
        time.sleep(2)
        timings = self.driver.execute_script("return window.performance.timing")

        # TODO: Save the performance.timing output as a file
        print(json.dumps(timings, indent=2))
        assert(True)

    def tearDown(self):
        # Stop gecko profiler recording
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + '2')
        # Stop video recording
        self.proc.send_signal(3)

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
        with io.open('cleopatra-profile.bin', 'w', encoding='utf-8') as f:
            f.write(recording)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
