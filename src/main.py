import os
import glob
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

from pdf2image import convert_from_path

filePaths = glob.glob(os.getcwd() + '*/*.pdf',
                      recursive=False)  # searching for all .pdf files recursively, returns an array of files with their absolute paths
fileIndex = 0
directory = glob.glob(os.getcwd())[0]


def select_folder():
    global directory
    directory = filedialog.askdirectory()
    refresh_folder()


def refresh_folder():
    global filePaths
    global directory

    lbFileSelection.delete(0, 'end')  # deletes all files in lb

    os.chdir(directory)
    filePaths = glob.glob(os.getcwd() + '*/*.pdf',
                          recursive=False)  # searching for all .pdf files recursively, returns an array of files with their absolute paths

    for path in filePaths:
        path = path.split("\\")[-1]
        lbFileSelection.insert('end', path)  # inserting each word into tk listbox


def convert_selection():
    # try:
    global filePaths
    global fileIndex

    path = filePaths[fileIndex]
    print(path)

    # value = lbFileSelection.get(lbFileSelection.callbackFileSelection())  # getting the path of the selected file
    # selectionLabel.set(value)  # setting the text to display

    # filename = path.split("\\")[-1]
    # print(filename)

    # TODO fix convert to images function

    images = convert_from_path(path)  # converting the file to images; argument here is the filename itself NOT the path

    page = 0

    path = os.path.join(os.getcwd(), filename[:-4])
    print(path)
    os.makedirs(path, exist_ok=True)

    for img in images:  # saving each page as .jpg in the folder
        page += 1
        print(page)
        print(path + '\\' + str(page) + '.jpg')
        img.save(path + '\\' + str(page) + '.jpg', 'JPEG')

    # try:

    if zipFolder:
        shutil.make_archive(path, "zip", path)


def callbackFileSelection(event):  # aka
    # value = listbox.get(lb.curselection())   	# getting the path of the selected file
    # selection_label.set(value)				# setting the text to display
    global filePaths

    if len(filePaths) == 0:
        messagebox.showinfo(title="Result", message="Please select a folder containing .pdf files.")

    else:

        selection = event.widget.curselection()

        global fileIndex
        fileIndex = selection[0]


window = tk.Tk()  # creating a tk application

window.title('PDFtoImage')  # title of the program window

window.geometry('600x400')  # defining the window size

# frames


leftFrame = tk.Frame(window)
leftFrame.pack(side='left')

rightFrame = tk.Frame(window)
rightFrame.pack(side='right')

bottomFrame = tk.Frame(window)
bottomFrame.pack(side='bottom')

bottomLeftFrame = tk.Frame(bottomFrame)
bottomLeftFrame.pack(side='left')

bottomRightFrame = tk.Frame(bottomFrame)
bottomRightFrame.pack(side='right')

# user interface elements

selectionLabel = tk.Label(window, bg='blue', fg='white', font=('Arial', 14))
selectionLabel.pack(side="top", fill="x", padx=10, pady=10)

lbFileSelection = tk.Listbox(window, width=30)  # creating a listbox
lbFileSelection.bind("<<ListboxSelect>>",
                     callbackFileSelection)  # callback function for listbox ... executes when you select an entry
lbFileSelection.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, ipady=6)  # outer padding for the listbox/listview

refreshButton = tk.Button(bottomLeftFrame, text='Refresh', width=15, height=2, command=refresh_folder)
refreshButton.pack(side="left", padx=10, pady=10)

selectFolderButton = tk.Button(bottomLeftFrame, text='Select folder', width=15, height=2, command=select_folder)
selectFolderButton.pack(side="left", padx=10, pady=10)

convertPdfButton = tk.Button(bottomLeftFrame, text='Convert', width=15, height=2, command=convert_selection)
convertPdfButton.pack(padx=10, pady=10)

zipFolder = False
zipFolderCheckbox = tk.Checkbutton(bottomRightFrame, text='Create zipped folder', variable=zipFolder, onvalue=1,
                                   offvalue=0)
zipFolderCheckbox.pack(padx=10, pady=10)

refresh_folder()

window.mainloop()
