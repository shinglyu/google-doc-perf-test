__author__ = 'shako'
from recordscreen import video_capture_line
import subprocess
import time
proc = subprocess.Popen(video_capture_line(15, 0, 0, 1920, 1080, ":0.0", "h264_fast", "./tmp.mkv"))

time.sleep(10)

proc.send_signal(3)

