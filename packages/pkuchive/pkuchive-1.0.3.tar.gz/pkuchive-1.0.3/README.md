# pkuchive
 [![Build Status](https://travis-ci.org/enkerewpo/pkuchive.svg?branch=master)](https://travis-ci.org/enkerewpo/pkuchive)
 
A tool for OIer to tag the archive folder provided by PKU openjudge achieve service.

Written by [Kvar_ispw17](mailto:enkerewpo@gmail.com) on Python 2.7
## What is this ?
When you download your archive from PKU openjudge website, you will receive a folder with only problems' number in it.
Under the `pkuchive`'s help, your folder will be tag-on by the problems' titles which provides a pretty archive folder.
```
BEFORE:                                AFTER:
YOUR FOLDER                            YOUR FOLDER
   |----------- 1001                      |----------- 1001 A+B Problem
   |----------- 1002                      |----------- 1002 Exponentiation
   |----------- 1003                      |----------- 1003 487-3279
   |----------- 1004                      |----------- 1004 Hangover
   ...                                    ...
```

current version `1.0.3` release on 2017.9.16
## Setup
### 1. Get your POJ archive
Goto [PKU JudgeOnline](http://poj.org/) and login. Click the link `archive` on the right to download the `*.tgz` file.
### 2. Download Python
Goto [https://www.python.org/downloads/](https://www.python.org/downloads/) and choose __3.x version of Python__ to download.
Python is required to run the pkuchive program. Remember to install Python.
### 3. Get release of pkuchive
Visit [https://github.com/Enkerewpo/pkuchive/releases](https://github.com/Enkerewpo/pkuchive/releases) to get pkuchive's latest version.
Once you have unziped the release file at some dirctory on you computer, __that dirctory__ will stayed being your __work dir__.

## Using pkuchive
in root user and type this in your shell:
```
$ pip install pkuchive
```

## Startup

```
$ pkuchive

pkuchive usage:
     -i [dir] : selection the directory that contains your
                problems code folders           
     -h       : show this helping page
     -ver     : show the version of pkuchive
```

## Change log
### 2017.7.6 
  fixed filename for Chinese character by using decode UTF-8 [Kvar_ispw17].
