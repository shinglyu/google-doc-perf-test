import json
import time
from lib.perfBaseTest import PerfBaseTest

class TestGoogleDocSample(PerfBaseTest):

    def setUp(self):
        super(TestGoogleDocSample, self).setUp()
        self.docUrl = "https://docs.google.com/document/d/1HXDdOQuxQiX1bSrpAs4hJfTaim1iLO_xB01nokb0wT0/edit?usp=sharing"
        self.driver.get(self.docUrl)
        time.sleep(5)
        self.video_recording_obj.capture_screen(self.video_output_sample_1_fp, self.img_sample_dp, self.output_name + "_sample_1.jpg")

    def test_load(self):

        # Recording start marker
        self.driver.execute_script("var teststart = function(){document.getElementById('docs-branding-logo').style.backgroundColor = 'red'}; teststart()");
        time.sleep(5)
        timings = self.driver.execute_script("return window.performance.timing")

        # TODO: Save the performance.timing output as a file
        print(json.dumps(timings, indent=2))
        assert(True)

    def tearDown(self):
        self.video_recording_obj.capture_screen(self.video_output_sample_2_fp, self.img_sample_dp, self.output_name + "_sample_2.jpg")
        super(TestGoogleDocSample, self).tearDown()
