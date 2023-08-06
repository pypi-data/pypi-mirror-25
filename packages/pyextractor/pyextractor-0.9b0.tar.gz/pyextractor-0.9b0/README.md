# PyExtractor

Extractor is a command line program to extract data from pdf, images, using OCR,GROK patterns, YAML and multiprocessing. 
The goal of this application is collect data, extract and organize the results in csv file.

## Getting Start

These instructions will get you a copy of the project and running on your local machine.

### Installing

A instruction to installing your environment at **Ubuntu/Debian**

Only tested in Ubuntu with python3


```bash
sudo apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev
```
```bash
pip install pyextract
```

## Usage

The application has the follow workflow:
    - Download file
    - Extract text from file
    - Extract patterns
    - Write a csv file 

### Configuration file **config.yml**

This file is very important to application work is a file where reside all configurations, like: header of csv, order of columns, patterns to extract from file, ...
The [syntax](http://pyyaml.org/wiki/PyYAMLDocumentation#YAMLsyntax) of this file use the rules o [YAML](https://en.wikipedia.org/wiki/YAML).

Main Parameters:

**DEBUG**: Enable/Disable Debug output at stdout

**NUM_WORKERS**: Number of cores to processing

**patterns**: [Grok Patterns](https://github.com/garyelephant/pygrok/tree/master/pygrok/patterns).

**sequence**: The sequence is used to reference columns of csv related to patterns, and another configurations.

**See folder sample for example of use**.

## Built With

- Python 3.5
- [PyGrok](https://github.com/garyelephant/pygrok)
- [Textract](https://github.com/deanmalmgren/textract)

## Author

* **Marlon Petry** - *Initial work* - [Extractor](https://github.com/petryx/pyextractor)
* **Nhan Petry** - *Inspiration and first user* [Extractor](https://github.com/petryx/pyextractor)

## Acknowledgments

Please give us your feedback of use, it is very important to keep developing this tool.


## License


Copyright 2017 Marlon Petry

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
    PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
                                         PROCUREMENT OF SUBSTITUTE GOODS OR
                                         SERVICES; LOSS OF USE, DATA, OR
                                         PROFITS; OR BUSINESS INTERRUPTION)
    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.










