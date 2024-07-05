from tkinter import *
from tkinter.filedialog import askopenfilename 
from PIL import ImageTk, Image

# helper class
class Binary():

    # position index counts from 0 and right side
    def get_bit_val_at_position(num, pos):
        return (num >> pos) & 1
    


class ImportedImage():
    def __init__(self, img_path, img_label, root_window_widget):
        self.img_path = img_path
        self.img_label = img_label
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
        imageTk = ImageTk.PhotoImage(self.img)
        
        #WITHOUT THESE NEXT THREE LINES NOTHING WILL BE UPDATED
        self.img_label.configure(image= imageTk)
        self.img_label.image = imageTk
        self.root_window_widget.update_idletasks() 

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
    
# --- Main --- 

window = Tk()
scrollbar = Scrollbar(window)
scrollbar.grid(row=0,column=2)
canvas = Canvas(window)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=0,column=0)
img_label = Label(canvas)
img_label.grid(row=1, column=0)
#img_label.grid_anchor(anchor=CENTER)


#img_path_label = Label(window, text=img_path)
#img_path_label.grid(row=0, column=1, padx=10)

imported_image = ImportedImage
def import_image():
    global imported_image
    imported_image = ImportedImage(img_path=askopenfilename(initialdir="/",title="Choose the image"), img_label=img_label, root_window_widget=window)     


change_image_btn = Button(canvas, text="Change image", command=lambda: import_image())
red_filter_btn = Button(canvas,text="Red filter", command=lambda: imported_image.change_image_pixels_rgb_value(r=255))
green_filter_btn = Button(canvas,text="Green filter", command=lambda: imported_image.change_image_pixels_rgb_value(g=255))
blue_filter_btn = Button(canvas,text="Blue filter", command=lambda: imported_image.change_image_pixels_rgb_value(b=255))
original_image_btn = Button(canvas,text="Original", command=lambda: imported_image.construct_show_original_image())

binary_thresholding_slider = Scale(canvas,from_=0, to=255, variable=255)
inversion_btn = Button(canvas,text="Color inversion", command=lambda: imported_image.inverse_image_color())
gray_code_btn = Button(canvas,text="Gray code", command=lambda: imported_image.image_gray_code())

txt = Text(canvas,height=10,width=40)
def set_lsb_to_widget():
    lsb_data = imported_image.extract_lsb_data()
    txt.delete("1.0", END) # to clear txt
    txt.insert("1.0",lsb_data)

lsb_btn = Button(canvas,text="Extract LSB text", command=lambda: set_lsb_to_widget())
txt.grid(row=5, column=1)


def thresholding_slider_listener(Any):
    slider_val = binary_thresholding_slider.get()
    imported_image.binary_threshold_image(slider_val)

binary_thresholding_slider.configure(command=thresholding_slider_listener)

bit_plane_slider = Scale(from_=0, to=7)

def bit_plane_listener(Any):
    slider_val = bit_plane_slider.get()
    imported_image.image_bit_plane(slider_val)

bit_plane_slider.configure(command=bit_plane_listener)

change_image_btn.grid(row=4,column=3)
red_filter_btn.grid(row=2,column=0, padx=10)
green_filter_btn.grid(row=2, column=1, padx=10)
blue_filter_btn.grid(row=2, column=2, padx=10)
original_image_btn.grid(row=2, column=3, padx=10)

lsb_btn.grid(row=4,column=0)

binary_thresholding_slider.grid(row=2,column=4)
bit_plane_slider.grid(row=3, column=4)

inversion_btn.grid(row=3, column=0)
gray_code_btn.grid(row=3, column=1)

# To disallow window resize
#window.resizable(width=False, height=False)
window.mainloop()


#def main():


#if __name__ == "__main__":
    #main()
