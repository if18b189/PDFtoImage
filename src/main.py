"""PDFtoImage

Convert Pdf files into image files(.jpeg, .png, .ppm, .tiff).
Show Information about the Pdf file.

Classes:

    PdfInfo

Functions:

    selectFolder()
    refreshFolder()
    convertSelection()
    getPdfInfo()
    getPath() -> string
    callbackFileSelection(event)
    selectOutputType() -> string

Misc variables:

    filePaths
    fileIndex
    path
    directory

"""

import re
import os
import glob
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from fpdf import FPDF
from PIL import Image

from pdf2image import convert_from_path

filePaths = glob.glob(os.getcwd() + '*/*.pdf',
                      recursive=False)  # searching for all .pdf files recursively, returns an array of files with
# their absolute paths
fileIndex = 0
path = ""
directory = glob.glob(os.getcwd())[0]


class PdfInfo:
    """ 
    This class contains information about the pdf file.

    Attributes:
        infoList (str[]): A list of the metadata, extracted from the pdf.
        pages (int): Number of pages.
    """

    def __init__(self, pdfFilePath):
        """
        The constructor for PdfInfo class.

        Parameters:
            pdfFilePath (str): Path of the pdf file.
        """
        self.infoList = []
        self.pages = 0

        proc = subprocess.Popen('pdfinfo ' + pdfFilePath, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            self.infoList.append(line.decode("utf8").strip())  # .strip() removes '\r\n'
        print(self.infoList)

    def showInfoWindow(self):
        """
        Opens a new window containing all Information extracted from the pdf.
        """
        # Toplevel object which will
        # be treated as a new window
        newWindow = tk.Toplevel(master)

        # sets the title of the
        # Toplevel widget
        newWindow.title("PDF Info")  # add filename - Info

        # sets the geometry of toplevel
        newWindow.geometry("")  # "" means it will automatically resize

        text = tk.Text(newWindow)
        for lines in self.infoList:
            text.insert(tk.INSERT, lines + "\n")
        text.pack(padx=10, pady=10)

    def getPages(self):  # maximum amount of pages
        """
        Gets and returns the number of pages.

        Returns:
            pages (int): Number of pages.
        """
        self.pages = int(re.search(r'\d+', self.infoList[8]).group())
        return self.pages


def selectFolder():
    """
    Prompts the user to select a directory/folder.
    """
    global directory
    directory = filedialog.askdirectory()
    refreshFolder()


def refreshFolder():
    """
    Scans(recursively) the current directory for pdf files, updates listbox entries, resets "conversionProgressBar".
    """
    global filePaths
    global directory

    lbFileSelection.delete(0, 'end')  # deletes all files in lb

    os.chdir(directory)  # changing cwd
    allPdfPaths = glob.glob(os.getcwd() + '*/*.pdf',
                            recursive=False)  # searching for all .pdf files recursively, returns an array of files
    # with their absolute paths

    for pdfPath in allPdfPaths:
        pdfPath = pdfPath.split("\\")[-1]  # splitting all the .pdf up
        lbFileSelection.insert('end', pdfPath)  # inserting each word into tk listbox

    conversionProgressBar["value"] = 0  # resetting the progressbar


def convertImgToPdf():

    folder = filedialog.askdirectory()

    imagePaths = glob.glob(folder + '*/*.jpg',
                           recursive=False)  # searching for all .jpeg files in the folder

    cover = Image.open(imagePaths[0])

    width, height = cover.size

    pdf = FPDF(unit="pt", format=[width, height])

    for page in imagePaths:
        pdf.add_page()
        pdf.image(page, 0, 0)

    pdf.output(os.getcwd() + "test.pdf", "F")

    print("done")

def convertSelection():
    """
    Converts the selected Pdf file into images.
    """
    # TODO: empty folder is being created when you dont select a filetype
    # TODO: split project up into multiple files?
    # TODO: selecting files after selecting a different folder -> indexerror: list index out of range

    # try:

    refreshFolder()  # fixed the following issue: it is necessary to refresh between multiple conversions

    global path

    # value = lbFileSelection.get(lbFileSelection.callbackFileSelection())  # getting the path of the selected file
    # selectionLabel.set(value)  # setting the text to display

    # print(path.split("\\")[-1])

    images = convert_from_path(path)  # converting the file to images

    page = 0
    maxPage = PdfInfo(getPath()).getPages()
    conversionProgressBar["maximum"] = maxPage

    filename = path.split("\\")[-1]  # getting the original .pdf filename for the "images"-folder
    path = os.path.join(os.getcwd(), filename[:-4])

    outputFileType = selectOutputType()  # .jpeg
    outputFolder = path + "_" + outputFileType[1:]  # <example folder name>_jpeg

    print(path)

    os.makedirs(outputFolder, exist_ok=True)

    for img in images:  # saving each page as .jpg in the folder

        conversionProgressBar["value"] += 1

        page += 1
        print(page)
        print(outputFolder + '\\' + str(page) + outputFileType)
        img.save(outputFolder + '\\' + str(page) + outputFileType, outputFileType[1:].upper())  # ( directory + name ,
        # filetype 'JPEG')

    # try:

    # zipping option
    if zipFolder.get() == 1:
        shutil.make_archive(outputFolder, "zip", outputFolder)


def getPdfInfo():
    """
    Opens a window that contains pdf metadata.
    """
    PdfInfo(getPath()).showInfoWindow()


def getPath():
    """
    Get the pdf file path.

    Returns:
        path (str): A string containing the pdfs file path.
    """
    global path
    return path


def callbackFileSelection(event):
    """
    Is being called everytime the user selects a file from the listbox(lbFileSelection).

    Parameters:
        event (event): Triggers when you select an item from the specified listbox.
    """
    global filePaths
    global fileIndex
    global path

    if len(filePaths) == 0:
        messagebox.showinfo(title="Result", message="Please select a folder containing .pdf files.")

    else:

        selection = event.widget.curselection()
        print(selection)
        path = filePaths[selection[0]]
        print(filePaths)


def selectOutputType():
    '''
    Returns the selected image file type as a string.

    Returns:
        fileType (str): A string representing the filetype, ".jpeg" as an example.
    '''

    choice = fileTypeVar.get()
    fileType = ""
    if choice == 1:
        fileType = ".jpeg"

    elif choice == 2:
        fileType = ".png"

    elif choice == 3:
        fileType = ".ppm"

    elif choice == 3:
        fileType = ".tiff"

    else:
        messagebox.showerror("No file type selected", "Please select a file type before converting!")

    return fileType


master = tk.Tk()  # creating a tk application+

master.title('PDFtoImage')  # title of the program window

master.geometry("")  # defining the window size

# frames


leftFrame = tk.Frame(master)
leftFrame.pack(side='left')

rightFrame = tk.Frame(master)
rightFrame.pack(side='right', fill=tk.BOTH, expand=True)

bottomFrame = tk.Frame(master)
bottomFrame.pack(side='bottom', fill=tk.BOTH, expand=True)

middleFrame = tk.Frame(master)
middleFrame.pack(side='bottom', fill=tk.BOTH, expand=True)

controlsLeftFrame = tk.Frame(middleFrame)
controlsLeftFrame.pack(side='left')

controlsRightFrame = tk.Frame(middleFrame)
controlsRightFrame.pack(side='right')

# user interface elements

selectionLabel = tk.Label(master, bg='blue', fg='white', font=('Arial', 14))
selectionLabel.pack(side="top", fill="x", padx=10, pady=10)

lbFileSelection = tk.Listbox(master, width=30)  # creating a listbox
lbFileSelection.bind("<<ListboxSelect>>",
                     callbackFileSelection)  # callback function for listbox ... executes when you select an entry
lbFileSelection.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, ipady=6)  # outer padding for the listbox/listview

outputFileTypeLabel = tk.Label(rightFrame, text="Output file format:")
outputFileTypeLabel.pack(side="top", fill="x", padx=10, pady=10)

fileTypeVar = tk.IntVar()
fileTypeRBtn = tk.Radiobutton(rightFrame, text=".jpeg", variable=fileTypeVar,
                              value=1)
fileTypeRBtn.pack(side="top", padx=5, pady=5)

fileTypeRBtn2 = tk.Radiobutton(rightFrame, text=".png ", variable=fileTypeVar,
                               value=2)
fileTypeRBtn2.pack(side="top", padx=5, pady=5)

fileTypeRBtn3 = tk.Radiobutton(rightFrame, text=".ppm ", variable=fileTypeVar,
                               value=3)
fileTypeRBtn3.pack(side="top", padx=5, pady=5)

fileTypeRBtn4 = tk.Radiobutton(rightFrame, text=".tiff", variable=fileTypeVar,
                               value=4)
fileTypeRBtn4.pack(side="top", padx=5, pady=5)

refreshButton = tk.Button(controlsLeftFrame, text='Refresh', width=15, height=2, command=refreshFolder)
refreshButton.pack(side="left", padx=10, pady=10)

selectFolderButton = tk.Button(controlsLeftFrame, text='Select folder', width=15, height=2, command=selectFolder)
selectFolderButton.pack(side="left", padx=10, pady=10)

convertPdfButton = tk.Button(controlsLeftFrame, text='Convert', width=15, height=2, command=convertSelection)
convertPdfButton.pack(padx=10, pady=10)

zipFolder = tk.IntVar()
zipFolderCheckbox = tk.Checkbutton(controlsRightFrame, text='Create zipped folder', variable=zipFolder, onvalue=1,
                                   offvalue=0)
zipFolderCheckbox.pack(padx=10, pady=10)

conversionProgressBar = ttk.Progressbar(bottomFrame, orient="horizontal", length=120, mode="determinate")
conversionProgressBar.pack(side="right", padx=20, pady=10)

showInfoButton = tk.Button(bottomFrame, text='Show info', width=15, height=2, command=getPdfInfo)
showInfoButton.pack(side="left", padx=10, pady=10)

convertImageButton = tk.Button(bottomFrame, text='Convert Images', width=15, height=2, command=convertImgToPdf)
convertImageButton.pack(side="left", padx=10, pady=10)

refreshFolder()

master.mainloop()
