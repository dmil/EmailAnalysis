EmailAnalysis
=============

A toolkit to use the gmail API to download and analyze emails

## Getting Started

1. Navigate to the [Google Developer console](https://console.developers.google.com/apis/credentials) and create a new project, get service account credentials for that project. Save the json file it generates as `credentials/credentials.json`.

2. Copy `keys.json.example` into `keys.json` and fill out the oauth token and key.

3. Install packages
	```
	pipenv install
	```

4. Download emails into a sqlite database called `emails.db`
	```
	python downloader.py
	```

5. Run the jupyter notebook for analysis
	```
	pipenv run jupyter notebook EmailAnalysis.ipynb
	```

## Installing in another project

#### Install from master
`pipenv install -e git+git@github.com/dmil/EmailAnalysis.git#egg=emailanalysis`

#### Install from commit
`pipenv install -e git+git@github.com/dmil/EmailAnalysis.git@COMMIT_SHA#egg=emailanalysis`

where `COMMIT_SHA` is the hash of the commit you want to install from