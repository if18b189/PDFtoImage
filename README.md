# PDFtoImage

## Overview
I had to convert PDF files to image and decided to use this opportunity to start this project.

## Screenshots:

/

## Setup & Installation

The easiest way of installing this project is by using a conda environment.
I tried to install python-poppler with pip but didn't manage to make it work.

If you are using Windows and do not want to install conda you could also download the latest poppler release and add the directory of the "bin" folder to your environment variables(PATH).

###Instructions using conda:
1. Open up a terminal/command line 
2. Navigate into the projects directory
3. Use `conda install -r requirements.txt` to install the required modules/libraries
3. Now you should be ready to start the program

Alternatively you can try the more extensive instructions on installing poppler here:
https://pdf2image.readthedocs.io/en/latest/installation.html

## Usage & Details

1. Open up a terminal/command line 
2. Navigate into the project directory
3. Run the script by typing `python ./src/main.py`
4. Now a window should appear, where you can select the PDF file you want to convert.

## Roadmap:
- [ ] add more buttons and functionalities
- [ ] select a range of pages to convert
- [ ] select a specific page to convert
