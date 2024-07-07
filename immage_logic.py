from tkinter import *
from PIL import ImageTk, Image
#import gui

# helper class
class Binary():

    # position index counts from 0 and right side
    def get_bit_val_at_position(num, pos):
        return (num >> pos) & 1
    


class ImageProcessing():
    def __init__(self, img_path, canvas,root_window_widget):
        self.img_path = img_path
        self.image_canvas = canvas
        self.is_image_widget_created = False
        self.root_window_widget = root_window_widget
        self.construct_show_original_image()


    def construct_original_image(self):
        self.img = Image.open(self.img_path)
        #self.img = self.img.resize((500,320))
        
    
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
            # binary in this context is either zero pixel light (0) *black color* or full pixel light (255) *white color* 
            binary = 0
            if average > 255-threshold:
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

    def image_gray_code(self):
        self.construct_original_image()
        pixels = list(self.img.getdata())
        for i in range(len(pixels)):
            #average = (pixels[i][0]+pixels[i][1]+pixels[i][2])/3
            #average = int(average)
            #pixels[i] = (average ^ (average>>1), average ^ (average>>1), average ^ (average>>1))
            pixels[i] = (pixels[i][0] ^ (pixels[i][0]>>1), pixels[i][1] ^ (pixels[i][1]>>1), pixels[i][2] ^ (pixels[i][2]>>1))
        self.img.putdata(pixels)
        self.update_image_label()


    def image_bit_plane(self, bit_pos):

        self.construct_original_image()
        pixels = list(self.img.getdata())
        for i in range(len(pixels)):
            average = (pixels[i][0]+pixels[i][1]+pixels[i][2])/3
            average = int(average)
            # either 0 or 255
            binary = Binary.get_bit_val_at_position(average, bit_pos) *255
            pixels[i] = (binary,binary,binary)

        self.img.putdata(pixels)
        self.update_image_label()

    def update_image_label(self):
        resized_img = self.img
        resized_img = resized_img.resize((500,320))
        imageTk = ImageTk.PhotoImage(resized_img)
        self.imageTk = imageTk # to prevent garbage collection
        #self.image_canvas.delete("imported_image") # to prevent stack of images
        if self.is_image_widget_created == True:
            self.image_canvas.itemconfig('imported_image', image=self.imageTk)
        else:
            self.image_canvas.create_image(336,246, image=self.imageTk, tag="imported_image")
            self.is_image_widget_created = True

        #WITHOUT THESE NEXT TWO LINES NOTHING WILL BE UPDATED
        #self.img_canvas.image = imageTk
        #self.root_window_widget.update_idletasks() 

    # extracts Least Significant Bit hidden data from each pixel color LSB 
    def extract_lsb_data(self):
        self.construct_original_image()
        pixels = list(self.img.getdata())
        extracted_data = ""
        binary_str = ""
        for i in range(len(pixels)):
            #               A trick to get LSB
            binary_str += str(pixels[i][0] & 1)
            binary_str += str(pixels[i][1] & 1)
            binary_str += str(pixels[i][2] & 1)
        for i in range(0, len(binary_str), 8):
            binary_chr = binary_str[i:i+8]
            num = int(binary_chr,2)
            extracted_data += chr(num)
        return extracted_data
    

