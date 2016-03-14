Google Doc Performance Test
===========================
A Framework for testing Google Doc performance on Firefox

# Installation
* Install Firefox
* Install Selenium for Python
* Install video recording codes and libs
* Install video recording main program

```
virtualenv venv
source venv/bin/activate

pip install selenium
For Ubuntu:
sudo apt-get install wget libav-tools ffmpeg libavc1394-0 libavformat-extra-53 libavfilter2 libavutil-extra-51 mencoder libavahi-common-data

For Mac OS:
brew install ffmpeg
brew install libav

wget http://www.davidrevoy.com/data/documents/recordscreen_12-04.zip
unzip recordscreen_12-04.zip
rm recordscreen_12-04.zip
chmod +x recordscreen.py

```

# Setup 
* Create a google doc, share it to the public (don't require login)
* Copy the link and paste it to `self.docUrl` in `testperf::setUp`

# Usage

```
python testperf.py
```
