import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
import json
import subprocess
from recordscreen import video_capture_line
import time

class GoogleDocPerfTest(unittest.TestCase):
    _profile_name = "test"

    proc = None

    def setUp(self):
        self.proc = subprocess.Popen(video_capture_line(300, 0, 0, 1920, 1080, ":0.0", "h264_fast", "./tmp.mkv"))
        #self.docUrl = "https://docs.google.com/document/d/1HXDdOQuxQiX1bSrpAs4hJfTaim1iLO_xB01nokb0wT0/edit?usp=sharing"
        self.docUrl = "https://docs.google.com/document/d/1V17WzeUGbUTc4oqqS3IvnRLCC9Xs79p6CeDyKo0LBq0/edit"
        #self.driver = webdriver.Firefox()
        chromedriver = "./chromedriver"
        self.driver = webdriver.Chrome(chromedriver)
        self.driver.get(self.docUrl)

    def test_load(self):

        # Recording start marker
        self.driver.execute_script("var teststart = function(){document.getElementById('docs-branding-logo').style.backgroundColor = 'red'}; teststart()");

        el = self.driver.find_elements_by_xpath("/body")
        element = self.driver.find_element_by_id("docs-table-menu")
        ActionChains(self.driver).move_to_element(element).click().perform()
        ActionChains(self.driver).move_to_element(element).move_by_offset(0,35).move_by_offset(100,0).move_by_offset(10,10).perform()
        time.sleep(2)
        grid = self.driver.find_element_by_xpath('//div[@class="goog-dimension-picker"]')
        ActionChains(self.driver).drag_and_drop_by_offset(grid, 50, 50).perform()
        #grid.click()
        #el.send_keys(Keys.COMMAND + 'a' + 'v')
        timings = self.driver.execute_script("return window.performance.timing")
        self.proc.send_signal(3)
        print(json.dumps(timings, indent=2))
        time.sleep(3)
        #assert(True)

    def tearDown(self):
        print('stopping')
        #self.driver.close()

if __name__ == "__main__":
    unittest.main()
