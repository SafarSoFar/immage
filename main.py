from tkinter import *
from PIL import ImageTk, Image

def change_pixels_rgb_value(pixels, r= -1, g= -1, b = -1):
    new_pixels = list() 
    for pix in pixels:
        # local values that are assigned to tuples
        new_r = r
        new_g = g
        new_b = b
        if r == -1:
            new_r = pix[0]
        if g == -1:
            new_g = pix[1]
        if b == -1:
            new_b = pix[2]
        new_pixels.append((new_r, new_g,new_b))
    
    return new_pixels

def main():
    window = Tk()
    greeting = Label(text="hello world")
    greeting.pack()

    image = Image.open("funny-cat.jpg")
    pixels = list(image.getdata())

    new_pixels = change_pixels_rgb_value(pixels, 255)


    image.putdata(data=new_pixels)
    image = ImageTk.PhotoImage(image)
    img_label = Label(window, image=image)
    img_label.pack()
    window.mainloop()

if __name__ == "__main__":
    main()
