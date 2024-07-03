from tkinter import *
from tkinter.filedialog import askopenfilename 
from PIL import ImageTk, Image



window = Tk()

img_label = Label(window)
img_label.pack()

img_path = ""

def set_image_path():
    global img_path
    img_path = askopenfilename(initialdir="/",title="Select the image")
    update_image_label()

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
    global img_path
    if img_path == "":   
        set_image_path()
        #return
    image = Image.open(img_path)
    image = image.resize((500,320))
    pixels = list(image.getdata())
    new_pixels = change_pixels_rgb_value(pixels, r,g,b)
    image.putdata(data=new_pixels)
    image = ImageTk.PhotoImage(image)
    '''
        WITHOUT THOSE NEXT THREE LINES NOTHING WILL BE UPDATED
    '''
    img_label.configure(image= image)
    img_label.image = image
    window.update_idletasks() 
    
image_path_btn = Button(text="Select the image", command=set_image_path)

red_filter_btn = Button(text="Red filter", command=lambda: update_image_label(r=255))
green_filter_btn = Button(text="Green filter", command=lambda: update_image_label(g=255))
blue_filter_btn = Button(text="Blue filter", command=lambda: update_image_label(b=255))
normal_filter_btn = Button(text="Original", command=lambda: update_image_label())

image_path_btn.pack()
red_filter_btn.pack()
green_filter_btn.pack()
blue_filter_btn.pack()
normal_filter_btn.pack()

# To disallow window resize
#window.resizable(width=False, height=False)
window.mainloop()


#def main():




#if __name__ == "__main__":
    #main()
