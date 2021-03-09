# PDFtoImage

## Overview
I had to convert a PDF file to image files and decided to use this opportunity to start this project.

## Screenshots:

/

## Setup & Installation

The easiest way of installing this project is by using a conda environment.
I tried to install python-poppler with pip but didn't manage to make it work.(had to download poppler separately)

If you are using Windows and do not want to install conda you could also download the latest poppler release and add the directory of the "bin" folder to your environment variables(PATH).

### Instructions using conda:

```
git clone https://github.com/if18b189/PDFtoImage
cd PDFtoImage
conda install -r requirements.txt
   > to install into the current environment
conda create --name <envName> --file requirements.txt 
   > to install into a new environment
```

Alternatively you can try the more extensive instructions on installing poppler here:
https://pdf2image.readthedocs.io/en/latest/installation.html

## Usage & Details

1. Open up a terminal/command line 
2. Navigate into the project directory
3. Run the script by typing `python ./src/main.py`
4. Now a window should appear, where you can select the PDF file you want to convert.

## Roadmap:
- [x] add more buttons and functionalities
- [ ] add options to convert into other formats (tiff, png, jpeg, pmm)
- [ ] select a range of pages to convert
- [ ] select a specific page to convert
