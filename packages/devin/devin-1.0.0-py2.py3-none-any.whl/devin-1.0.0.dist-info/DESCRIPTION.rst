# pypi starter project

[![Build Status](https://travis-ci.org/wuhaifengdhu/pypi-starter.svg?branch=master)](https://travis-ci.org/wuhaifengdhu/pypi-starter)
[![codecov](https://codecov.io/gh/wuhaifengdhu/pypi-starter/branch/master/graph/badge.svg)](https://codecov.io/gh/wuhaifengdhu/pypi-starter)

This is a template repository that you can use to quickly create a python application that can be built, tested, and released as an internal python module.

## Setting up a new repository from this template
**Create a directory and pull all the files in this template into it**

```bash
mkdir new_repo_name
cd new_repo_name
git init
git pull https://github.com/wuhaifengdhu/pypi-starter
```

## Build

*Linux*

```bash
virtualenv env
. env/bin/activate
pip install -e .
```

*Windows*
```bash
virtualenv env
env\Scripts\activate
pip install -e .
```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
# run the python tests
tox -r
```

## upload to pypi
* Register your account in ![pypi](https://pypi.org/)
* Create file .pypirc in your home folder with 600.    
```[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository=https://upload.pypi.org/legacy/
username=your_username
password=your_password

[pypitest]
repository=https://test.pypi.org/legacy/
username=your_username
password=your_password
``` 
* Upload your repository
```
Python setup.py bidet_wheel —universal
Twine upload dist/*
```        





