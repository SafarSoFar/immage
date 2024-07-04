from tkinter import *
from tkinter.filedialog import askopenfilename 
from PIL import ImageTk, Image
from array import array


class ImportedImage():
    def __init__(self, img_path, img_label, root_window_widget):
        self.img_path = img_path
        self.img_label = img_label
        self.root_window_widget = root_window_widget
        self.construct_show_original_image()


    def construct_original_image(self):
        self.img = Image.open(self.img_path)
        self.img.resize((500,320))
    
    def construct_show_original_image(self):
        self.construct_original_image()
        self.update_image_label()

    # changes pixel values (RGB) specified by parameters accordingly 
    def change_image_pixels_rgb_value(self,r= -1, g= -1, b = -1):

        self.construct_original_image()
        pixels = list(self.img.getdata())
        for i in range(len(pixels)):

            # local values that are assigned to tuples
            new_r = r
            new_g = g
            new_b = b

            if r == -1:
                new_r = pixels[i][0]
            if g == -1:
                new_g = pixels[i][1]
            if b == -1:
                new_b = pixels[i][2]
            pixels[i] = (new_r,new_g, new_b)
        self.img.putdata(pixels)
        self.update_image_label()


    # invokes on slider value change
    # sets each pixel either 0 or 255 depending on pixel brightness(rgb average) againt threshold
    def binary_threshold_image(self,threshold):
       
        self.construct_original_image()
        pixels = list(self.img.getdata())
        for i in range(len(pixels)):
            r = pixels[i][0]
            g = pixels[i][1]
            b = pixels[i][2]
            average = (r+g+b)/3
            # binary in this context is either zero pixel light (0) *black color* or full pixl light (255) *white color* 
            binary = 0
            if average > threshold:
                binary = 255
            pixels[i]=(binary,binary,binary)

        self.img.putdata(pixels)
        self.update_image_label()
    
    # pixel color inversion using full alpha constant 255
    def inverse_image_color(self):
        self.construct_original_image()
        pixels = list(self.img.getdata())
        for i in range(len(pixels)):
            pixels[i] = (255-pixels[i][0], 255-pixels[i][1], 255-pixels[i][2])
        self.img.putdata(pixels)
        self.update_image_label()

    def update_image_label(self):
        imageTk = ImageTk.PhotoImage(self.img)
        
        #WITHOUT THESE NEXT THREE LINES NOTHING WILL BE UPDATED
        self.img_label.configure(image= imageTk)
        self.img_label.image = imageTk
        self.root_window_widget.update_idletasks() 

    
# --- Main --- 

window = Tk()

img_label = Label(window)
img_label.grid(row=1, column=0, sticky=N)
img_label.grid_anchor(anchor=CENTER)

img_path = "No image path"
img = Image

#img_path_label = Label(window, text=img_path)
#img_path_label.grid(row=0, column=1, padx=10)


imported_image = ImportedImage(img_path="funny-cat.jpg", img_label=img_label, root_window_widget=window)

red_filter_btn = Button(text="Red filter", command=lambda: imported_image.change_image_pixels_rgb_value(r=255))
green_filter_btn = Button(text="Green filter", command=lambda: imported_image.change_image_pixels_rgb_value(g=255))
blue_filter_btn = Button(text="Blue filter", command=lambda: imported_image.change_image_pixels_rgb_value(b=255))
normal_filter_btn = Button(text="Original", command= imported_image.construct_show_original_image)
binary_thresholding_slider = Scale(from_=0, to=255)
inversion_btn = Button(text="Color inversion", command=imported_image.inverse_image_color)

def thresholding_slider_listener(Any):
    slider_val = binary_thresholding_slider.get()
    imported_image.binary_threshold_image(slider_val)

binary_thresholding_slider.configure(command=thresholding_slider_listener)


#image_path_btn.grid(row=0,column=0, padx=10)
red_filter_btn.grid(row=2,column=0, padx=10)
green_filter_btn.grid(row=2, column=1, padx=10)
blue_filter_btn.grid(row=2, column=2, padx=10)
normal_filter_btn.grid(row=2, column=3, padx=10)
binary_thresholding_slider.grid(row=2,column=4)
inversion_btn.grid(row=3, column=0)

# To disallow window resize
#window.resizable(width=False, height=False)
window.mainloop()


#def main():


#if __name__ == "__main__":
    #main()
