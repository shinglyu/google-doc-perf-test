Google Doc Performance Test
===========================
A Framework for testing Google Doc performance on Firefox

# Installation
* Install Firefox
* Install Selenium for Python

```
virtualenv venv
source venv/bin/activate

pip install selenium
```

# Setup 
* Create a google doc, share it to the public (don't require login)
* Copy the link and paste it to `self.docUrl` in `testperf::setUp`

# Usage

```
python testperf.py
```
