from tkinter import *
from tkinter.filedialog import askopenfilename 
from PIL import ImageTk, Image



window = Tk()

img_label = Label(window)
img_label.grid(row=1, column=0, sticky=N)
img_label.grid_anchor(anchor=CENTER)
#img_label.pack(anchor=CENTER)



img_path = "No image path"
img = Image

img_path_label = Label(window, text=img_path)
#img_label.pack()
img_path_label.grid(row=0, column=1, padx=10)

# simple boolean image path check 
def is_image_path_set():
    global img_path
    if img_path == "No image path":
        return False
    else:
        return True

# setting global img_path via file explorer
def set_image_path():
    global img_path
    #global img
    img_path = askopenfilename(initialdir="/",title="Select the image")
    img_path_label.configure(text=img_path)

# opens image from global img_path, sets size
def contruct_original_image():
    if is_image_path_set() == False:
        return False
    
    global img_path
    global img

    img = Image.open(img_path)
    img = img.resize((500,320))
    return True
    
# changes pixel values (RGB) specified by parameters accordingly 
def change_image_pixels_rgb_value(r= -1, g= -1, b = -1):
    
    if contruct_original_image() == False:
        return
    
    global img
    pixels = list(img.getdata())
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
    img.putdata(new_pixels)
    update_image_label()

'''def get_image_pixels_list(image_path):
    image = Image.open(image_path)
    image = image.resize((500,320))
    return list(image.getdata())'''

# invokes on slider value change
# sets each pixel either 0 or 255 depending on pixel brightness(rgb average) againt threshold
def binary_threshold_image(threshold):
    if contruct_original_image() == False:
        return
    
    global img
    pixels = list(img.getdata())
    new_pixels = list()
    for pix in pixels:
        r = pix[0]
        g = pix[1]
        b = pix[2]
        average = (r+g+b)/3
        #print(pix)
        binary = 0
        if average > threshold:
            binary = 255
        new_pixels.append((binary,binary,binary))
    img.putdata(new_pixels)
    update_image_label()

# shows original img without pixels modification
def show_original_image():
    if contruct_original_image() == False: # aborting on non-completed image contruction
        return
    update_image_label()


# updates image label via global img
def update_image_label():
    global img

    imageTk = ImageTk.PhotoImage(img)
    '''
        WITHOUT THOSE NEXT THREE LINES NOTHING WILL BE UPDATED
    '''
    img_label.configure(image= imageTk)
    img_label.image = imageTk
    window.update_idletasks() 
    
image_path_btn = Button(text="Select the image", command=set_image_path)

red_filter_btn = Button(text="Red filter", command=lambda: change_image_pixels_rgb_value(r=255))
green_filter_btn = Button(text="Green filter", command=lambda: change_image_pixels_rgb_value(g=255))
blue_filter_btn = Button(text="Blue filter", command=lambda: change_image_pixels_rgb_value(b=255))
normal_filter_btn = Button(text="Original", command= show_original_image)
binary_thresholding_slider = Scale(from_=0, to=255)

def thresholding_slider_listener(Any):
    slider_val = binary_thresholding_slider.get()
    binary_threshold_image(slider_val)

binary_thresholding_slider.configure(command=thresholding_slider_listener)


image_path_btn.grid(row=0,column=0, padx=10)
red_filter_btn.grid(row=2,column=0, padx=10)
green_filter_btn.grid(row=2, column=1, padx=10)
blue_filter_btn.grid(row=2, column=2, padx=10)
normal_filter_btn.grid(row=2, column=3, padx=10)
binary_thresholding_slider.grid(row=2,column=4)
'''image_path_btn.pack(anchor=N)
red_filter_btn.pack()
green_filter_btn.pack()
blue_filter_btn.pack()
normal_filter_btn.pack()'''

# To disallow window resize
#window.resizable(width=False, height=False)
window.mainloop()


#def main():


#if __name__ == "__main__":
    #main()
