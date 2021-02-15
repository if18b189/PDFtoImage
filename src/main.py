'''
https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/
https://github.com/oschwartz10612/poppler-windows/releases/

set enviroment var for poppler

     You will then have to add the bin/ folder to PATH or use

     poppler_path = r”C:\path\to\poppler-xx\bin” as an argument in convert_from_path.

'''

from pdf2image import convert_from_path
from tkinter import messagebox

import tkinter as tk

import glob
import os
import shutil


def convert_selection():
    # try:
    value = lb.get(lb.curselection())  # getting the path of the selected file
    selection_label.set(value)  # setting the text to display

    filename = value.split("\\")[-1]
    print(filename)

    images = convert_from_path(
        filename)  # converting the file to images; argument here is the filename itself NOT the path

    page = 0

    path = os.path.join(os.getcwd(), filename[:-4])
    print(path)
    os.makedirs(path, exist_ok=True)

    for img in images:  # saving each page as .img in the folder
        page += 1
        print(page)
        print(path + '\\' + str(page) + '.jpg')
        img.save(path + '\\' + str(page) + '.jpg', 'JPEG')

    # try:

    shutil.make_archive(path, "zip", path)


# except:
# 	Result = "zipping failed"
# 	messagebox.showinfo("Result", Result)

# except:
# 	Result = "No PDF found"
# 	messagebox.showinfo("Result", Result)

# else:
# 	Result = "success"
# 	messagebox.showinfo("Result", Result)


window = tk.Tk()  # creating a tk application
window.title('PDFtoImage')  # title of the program window

window.geometry('600x300')  # defining the window size

lb = tk.Listbox(window, width=100)  # creating a listbox

files = glob.glob(os.getcwd() + '/**/*.pdf',
                  recursive=True)  # searching for all .pdf files recursively, returns an array of files with their absolute paths

for file in files:  # inserting each file into the listbox
    lb.insert('end', file)

lb.pack(padx=10, pady=10)  # outer padding for the listbox/listview

selection_label = tk.StringVar()
l = tk.Label(window, bg='green', fg='yellow', font=('Arial', 12), width=60, textvariable=selection_label)
l.pack(padx=10, pady=10)

b1 = tk.Button(window, text='convert', width=15, height=2, command=convert_selection)
b1.pack(padx=10, pady=10)

print(files)

window.mainloop()

# def pdf2img():
#     try:
#         images = convert_from_path(str(e1.get()))
#         for img in images:
#             img.save('new_folder\output.jpg', 'JPEG')

#     except  :
#         Result = "NO pdf found"
#         messagebox.showinfo("Result", Result)

#     else:
#         Result = "success"
#         messagebox.showinfo("Result", Result)


# master = Tk()
# Label(master, text="File Location").grid(row=0, sticky=W)

# e1 = Entry(master)
# e1.grid(row=0, column=1)

# b = Button(master, text="Convert", command=pdf2img)
# b.grid(row=0, column=2,columnspan=2, rowspan=2,padx=5, pady=5)

# mainloop()
