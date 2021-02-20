import re
import os
import glob
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pdf2image import convert_from_path

filePaths = glob.glob(os.getcwd() + '*/*.pdf',
                      recursive=False)  # searching for all .pdf files recursively, returns an array of files with their absolute paths
fileIndex = 0
path = ""
directory = glob.glob(os.getcwd())[0]


class PdfInfo:
    def __init__(self, PdfFilePath):
        self.infoList = []
        self.pages = 0

        proc = subprocess.Popen('pdfinfo ' + path, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            self.infoList.append(line.decode("utf8").strip())  # .strip() removes '\r\n'
        print(self.infoList)

    def showInfoWindow(self):
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
        self.pages = int(re.search(r'\d+', self.infoList[8]).group())
        return self.pages


def selectFolder():
    global directory
    directory = filedialog.askdirectory()
    refreshFolder()


def refreshFolder():
    global filePaths
    global directory

    lbFileSelection.delete(0, 'end')  # deletes all files in lb

    os.chdir(directory)
    filePaths = glob.glob(os.getcwd() + '*/*.pdf',
                          recursive=False)  # searching for all .pdf files recursively, returns an array of files with their absolute paths

    for path in filePaths:
        path = path.split("\\")[-1]
        lbFileSelection.insert('end', path)  # inserting each word into tk listbox

    conversionProgressBar["value"] = 0  # resetting the progressbar


def convertSelection():
    # try:

    global path

    print(path)

    # value = lbFileSelection.get(lbFileSelection.callbackFileSelection())  # getting the path of the selected file
    # selectionLabel.set(value)  # setting the text to display

    # print(path.split("\\")[-1])

    images = convert_from_path(path)  # converting the file to images

    page = 0
    maxPage = PdfInfo(getPath()).getPages()
    conversionProgressBar["maximum"] = maxPage

    filename = path.split("\\")[-1]  # getting the original .pdf filename for the "images"-folder
    path = os.path.join(os.getcwd(), filename[:-4])
    print(path)
    os.makedirs(path, exist_ok=True)

    selectOutputType()

    for img in images:  # saving each page as .jpg in the folder

        conversionProgressBar["value"] += 1

        page += 1
        print(page)
        print(path + '\\' + str(page) + '.jpg')
        img.save(path + '\\' + str(page) + '.jpg', 'JPEG')

    # try:

    # zipping option
    if zipFolder.get() == 1:
        shutil.make_archive(path, "zip", path)


def getPdfInfo():
    PdfInfo(getPath()).showInfoWindow()


def getPath():
    global path
    return path


def callbackFileSelection(event):
    global filePaths
    global fileIndex
    global path

    if len(filePaths) == 0:
        messagebox.showinfo(title="Result", message="Please select a folder containing .pdf files.")

    else:

        selection = event.widget.curselection()
        path = filePaths[selection[0]]


def selectOutputType():
    choice = fileTypeVar.get()
    if choice == 1:
        fileType = ".jpeg"

    elif choice == 2:
        fileType = ".png"

    elif choice == 3:
        fileType = ".ppm"

    elif choice == 3:
        fileType = ".tiff"

    else:
        fileType = "Invalid selection"

    # return fileType
    return messagebox.showinfo('PythonGuides', f'You Selected {fileType}.')


master = tk.Tk()  # creating a tk application

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
fileTypeRBttn = tk.Radiobutton(rightFrame, text=".jpeg", variable=fileTypeVar,
                               value=1)
fileTypeRBttn.pack(side="top", padx=5, pady=5)

fileTypeRBttn2 = tk.Radiobutton(rightFrame, text=".png ", variable=fileTypeVar,
                                value=2)
fileTypeRBttn2.pack(side="top", padx=5, pady=5)

fileTypeRBttn3 = tk.Radiobutton(rightFrame, text=".ppm ", variable=fileTypeVar,
                                value=3)
fileTypeRBttn3.pack(side="top", padx=5, pady=5)

fileTypeRBttn4 = tk.Radiobutton(rightFrame, text=".tiff", variable=fileTypeVar,
                                value=4)
fileTypeRBttn4.pack(side="top", padx=5, pady=5)

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

refreshFolder()

master.mainloop()
