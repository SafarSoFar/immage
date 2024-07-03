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
pixels = list(image.getdata())
width, height = image.size

# reading pixel values
#for x in range (width):
    #for y in range (height):
        # -> print(pixels[x][2])

#for [x,y] in range(pixels):
    #print(x,y)
#image = Image.frombytes(size=[width,height], data=pixels, mode=w)
new_pixels = list()
for pix in pixels:
    new_pixels.append((pix[0], pix[1],255))
    #print(pix)

#image = Image.new(mode=image.mode, size=image.size)
image.putdata(data=new_pixels)
image = ImageTk.PhotoImage(image)
img_label = Label(window, image=image)
img_label.pack()
window.mainloop()
