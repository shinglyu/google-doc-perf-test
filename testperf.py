import unittest
from selenium import webdriver
import json

class GoogleDocPerfTest(unittest.TestCase):

    def setUp(self):
        self.docUrl = "https://docs.google.com/document/d/1HXDdOQuxQiX1bSrpAs4hJfTaim1iLO_xB01nokb0wT0/edit?usp=sharing"
        self.driver = webdriver.Firefox()
        self.driver.get(self.docUrl)

    def test_load(self):
        timings = self.driver.execute_script("return window.performance.timing")
        print(json.dumps(timings, indent=2))
        assert(True)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
