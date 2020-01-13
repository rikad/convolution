import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

#component
root = tk.Tk()
label1 = tk.Label( root, text="Tugas GPC - 14k")
label2 = tk.Label( root, text="10116908 - Rikad Fauzi Alawi")
label3 = tk.Label( root, text="10116908 - Indra Krisna Rama")
lineSize = tk.Scale( root, variable = tk.DoubleVar() , orient=tk.HORIZONTAL, from_=1, to=51, label="Ukuran Garis")
lines = tk.Scale( root, variable = tk.DoubleVar() , orient=tk.HORIZONTAL, from_=1, to=51, label="Detail Garis")
blur = tk.Scale( root, variable = tk.DoubleVar() , orient=tk.HORIZONTAL, from_=1, to=101, label="Color")

#canvas
canvas = tk.Canvas(root, height=250, width=300)
image_id = canvas.create_image(0,0, anchor=tk.NW)

#default config
lineSize.set(9)
lines.set(9)
blur.set(25)

def printConfig():
    if blur.get() % 2 == 0:
        blur.set(blur.get() + 1)

    if lineSize.get() % 2 == 0:
        lineSize.set(lineSize.get() + 1)

    print(lineSize.get())
    print(lines.get())
    print(blur.get())


def openfile():
    root.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.")))

    canvas.image_tk = ImageTk.PhotoImage(Image.open(root.filename))

    # configure the canvas item to use this image
    canvas.itemconfigure(image_id, image=canvas.image_tk)
    canvas.config(width=canvas.image_tk.width(), height=canvas.image_tk.height())

    #show editor
    proses()
    lineSize.pack(anchor=tk.CENTER)
    lines.pack(anchor=tk.CENTER)
    blur.pack(anchor=tk.CENTER)
    btnProses.pack()

def proses():

    printConfig()

    # 0) Open
    img = cv2.imread(root.filename)
    np.array(img, dtype=np.uint8)

    # 1) Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, lineSize.get(), lines.get())

    # 2) Color
    # color = cv2.bilateralFilter(img, 9, 300, 300)
    color = cv2.medianBlur(img, blur.get())

    # 3) Cartoon
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # 4) show
    cv2.destroyAllWindows()
    cv2.imshow("Cartoon", cartoon)

    # debug
    # cv2.destroyWindow("Cartoon")
    # cv2.imshow("Image", img)
    # cv2.imshow("color", color)
    # cv2.imshow("edges", edges)

#button
btnOpen = tk.Button(root, text ="Pilih File", command = openfile)
btnProses = tk.Button(root, text ="Proses", command = proses)

# show tkinter
root.minsize(800, 400)
label1.pack()
label2.pack()
label3.pack()
btnOpen.pack()
canvas.pack()
root.mainloop()