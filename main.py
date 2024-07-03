from tkinter import *
from PIL import ImageTk, Image

window = Tk()
greeting = Label(text="hello world")
greeting.pack()
#canvas = Canvas(window, width=100, height=100)
#canvas.pack()
#img = PhotoImage(file="funny-cat.jpg")
#canvas.create_image(img)
image = Image.open("funny-cat.jpg")
image = ImageTk.PhotoImage(image)
img_label = Label(window, image=image)
img_label.pack()
window.mainloop()
