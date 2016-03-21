Google Doc Performance Test
===========================
A Framework for testing Google Doc performance on Firefox

# Installation
* Install Firefox
* Install Selenium for Python
* Install video recording codes and libs
* Install video recording main program
* Install opencv

```
virtualenv venv
source venv/bin/activate

pip install selenium
sudo apt-get install wget libav-tools ffmpeg libavc1394-0 libavformat-extra-53 libavfilter2 libavutil-extra-51 mencoder libavahi-common-data

wget http://www.davidrevoy.com/data/documents/recordscreen_12-04.zip
unzip recordscreen_12-04.zip
rm recordscreen_12-04.zip
chmod +x recordscreen.py

wget https://github.com/bgirard/Gecko-Profiler-Addon/blob/master/geckoprofiler-signed.xpi?raw=true

wget https://github.com/Itseez/opencv/archive/3.0.0.zip

follow this link[http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/] to install the opencv
```

# Setup 
* Create a google doc, share it to the public (don't require login)
* Copy the link and paste it to `self.docUrl` in `testperf::setUp`

# Usage

```
python -m unittest tests.test_googledoc_sample
```

This will generate two files:
* `cleopetra-profile.bin`: the Gecko profile recording, can be viewed on https://cleopatra.io/
* `tmp.mkv`: the video recording
