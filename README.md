EmailAnalysis
=============

A toolkit to use the gmail API to download and analyze emails

## Getting Started

1. Install packages
```
pip install --upgrade google-api-python-client
pip install gflags
```

2. Download emails to /emails folder
```
python downloader.py
```

## STATUS

Not working, oauth library has been depracated

### TODO

- Switch authentication to use `google-auth` library: https://google-auth.readthedocs.io/en/latest/user-guide.html
- Improve README
- Add a python notebook layer for analysis