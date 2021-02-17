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
directory = glob.glob(os.getcwd())[0]


def show_Info():
    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel(master)

    # sets the title of the
    # Toplevel widget
    newWindow.title("PDF Info")  # add filename - Info

    # sets the geometry of toplevel
    newWindow.geometry("200x200")

    # A Label widget to show in toplevel
    Label(newWindow, text="This is a new window").pack()


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

    # print(path.split("\\")[-1])

    images = convert_from_path(path)  # converting the file to images

    page = 0

    proc = subprocess.Popen('pdfinfo ' + path, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        print(line.decode("utf8"))
    proc.wait()

    # filename = path.split("\\")[-1]  # getting the original .pdf filename for the "images"-folder
    # path = os.path.join(os.getcwd(), filename[:-4])
    # print(path)
    # os.makedirs(path, exist_ok=True)
    #
    # for img in images:  # saving each page as .jpg in the folder
    #     page += 1
    #     print(page)
    #     print(path + '\\' + str(page) + '.jpg')
    #     img.save(path + '\\' + str(page) + '.jpg', 'JPEG')
    #
    # # try:
    #
    # # zipping option
    # if zipFolder.get() == 1:
    #     shutil.make_archive(path, "zip", path)


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


master = tk.Tk()  # creating a tk application

master.title('PDFtoImage')  # title of the program window

master.geometry('600x400')  # defining the window size

# frames


leftFrame = tk.Frame(master)
leftFrame.pack(side='left')

rightFrame = tk.Frame(master)
rightFrame.pack(side='right')

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

refreshButton = tk.Button(controlsLeftFrame, text='Refresh', width=15, height=2, command=refresh_folder)
refreshButton.pack(side="left", padx=10, pady=10)

selectFolderButton = tk.Button(controlsLeftFrame, text='Select folder', width=15, height=2, command=select_folder)
selectFolderButton.pack(side="left", padx=10, pady=10)

convertPdfButton = tk.Button(controlsLeftFrame, text='Convert', width=15, height=2, command=convert_selection)
convertPdfButton.pack(padx=10, pady=10)

zipFolder = tk.IntVar()
zipFolderCheckbox = tk.Checkbutton(controlsRightFrame, text='Create zipped folder', variable=zipFolder, onvalue=1,
                                   offvalue=0)
zipFolderCheckbox.pack(padx=10, pady=10)

progressBar = ttk.Progressbar(bottomFrame, orient="horizontal", length=120, mode="determinate")
progressBar.pack(side="right", padx=20, pady=10)

showInfoButton = tk.Button(bottomFrame, text='Show info', width=15, height=2, command=show_Info)
showInfoButton.pack(side="left", padx=10, pady=10)

refresh_folder()

master.mainloop()
