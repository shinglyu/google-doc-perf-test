import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import json
import subprocess
from recordscreen import video_capture_line
import time

class GoogleDocPerfTest(unittest.TestCase):
    _profile_name = "test"

    proc = None

    def setUp(self):
        self.proc = subprocess.Popen(video_capture_line(300, 0, 0, 1920, 1080, ":0.0", "h264_fast", "./tmp.mkv"))
        self.docUrl = "https://docs.google.com/document/d/1V17WzeUGbUTc4oqqS3IvnRLCC9Xs79p6CeDyKo0LBq0/edit"
        #self.docUrl = "https://docs.google.com/document/d/1EpYUniwtLvBbZ4ECgT_vwGUfTHKnqSWi7vgNJQBemFk/edit"
        self.driver = webdriver.Firefox()
        chromedriver = "./chromedriver"
        #self.driver = webdriver.Chrome(chromedriver)
        self.driver.get(self.docUrl)

    def test_load(self):

        # Recording start marker
        self.driver.execute_script("var teststart = function(){document.getElementById('docs-branding-logo').style.backgroundColor = 'red'}; teststart()");
                
        ## this is case for scrolling down
        page = self.driver.find_element_by_xpath('//div[@class="kix-appview-editor"]')
        for p in range(100):
            page.send_keys(Keys.PAGE_DOWN)

        ## this is case for creating table
        element = self.driver.find_element_by_id("docs-table-menu")
        for i in range(1):
        	ActionChains(self.driver).move_to_element(element).click().perform()
        	ActionChains(self.driver).move_to_element(element).move_by_offset(0,35).perform()
        	time.sleep(3)
        	grid = self.driver.find_element_by_xpath('//div[@class="goog-dimension-picker"]')
        	#ActionChains(self.driver).drag_and_drop_by_offset(grid, 50, 50).perform()
        	#ActionChains(self.driver).move_to_element(grid).click_and_hold(on_element=None).move_by_offset(80, 80).release(on_element=None).perform()
        	ActionChains(self.driver).move_to_element(grid).move_by_offset(200,200).perform()
        	grid.click()        
        
        time.sleep(3)
        
        timings = self.driver.execute_script("return window.performance.timing")
        self.proc.send_signal(3)
        print(json.dumps(timings, indent=2))
        #assert(True)

    def tearDown(self):
        print('stopping')
        #self.driver.close()

if __name__ == "__main__":
    unittest.main()
