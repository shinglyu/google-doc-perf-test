import unittest
from selenium import webdriver
import json
import subprocess
from recordscreen import video_capture_line

class GoogleDocPerfTest(unittest.TestCase):

    proc = None

    def setUp(self):
        self.proc = subprocess.Popen(video_capture_line(300, 0, 0, 1920, 1080, ":0.0", "h264_fast", "./tmp.mkv"))
        self.docUrl = "https://docs.google.com/document/d/1HXDdOQuxQiX1bSrpAs4hJfTaim1iLO_xB01nokb0wT0/edit?usp=sharing"
        self.driver = webdriver.Firefox()
        self.driver.get(self.docUrl)

    def test_load(self):
        timings = self.driver.execute_script("return window.performance.timing")
        self.proc.send_signal(3)
        print(json.dumps(timings, indent=2))
        assert(True)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
