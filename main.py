from tkinter import *
from PIL import ImageTk, Image



window = Tk()

img_label = Label(window)
img_label.pack()


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

def update_image_label(r=-1,g=-1,b=-1):
    image = Image.open(r"funny-cat.jpg")
    pixels = list(image.getdata())
    new_pixels = change_pixels_rgb_value(pixels, r,g,b)
    image.putdata(data=new_pixels)
    image = ImageTk.PhotoImage(image)
    
    '''
        WITHOUT THOSE THREE LINES NOTHING WILL BE UPDATED
    '''
    img_label.configure(image= image)
    img_label.image = image
    window.update_idletasks() 


    


red_filter_btn = Button(text="Red filter", command=lambda: update_image_label(r=255))
green_filter_btn = Button(text="Green filter", command=lambda: update_image_label(g=255))
blue_filter_btn = Button(text="Blue filter", command=lambda: update_image_label(b=255))

red_filter_btn.pack()
green_filter_btn.pack()
blue_filter_btn.pack()

window.mainloop()


#def main():




#if __name__ == "__main__":
    #main()
