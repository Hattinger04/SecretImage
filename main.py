# tkinter provides GUI objects and commands
import tkinter as tk
import tkinter.ttk as ttk
# math provides some functions (ceil, floor)
import math
# Python Imaging Library (PIL) provides commands
# to comfortably open and save bitmap files
from PIL import Image, ImageTk
import io

# An object (root) is created which represents the window.
# Its title and full screen property are set.
root = tk.Tk()
root.title("Steganography with bitmaps")
root.wm_state("zoomed")


# The labels used to interact with the user are cleared.
def ClearFeedbackLabels():
    LabelSecretFeedback["text"] = ""
    LabelModeFeedback["text"] = ""


# This function is invoked when the user clicks the button
# "Load secret from file".
# It tries to open a textfile with the name specified in the
# corresponding entry field. Further, it tells the user
# whether the loading of the textfile succeeded and, if so,
# prints its contents in the text field below.
def ButtonSecretLoadClick():
    ClearFeedbackLabels()
    try:
        with open(PathSecret.get(), mode="rt", encoding="utf-8") as tf:
            secret = tf.read()
    except:
        LabelSecretFeedback["text"] = "An error occurred while reading the file."
        TextSecret.delete("1.0", "end")
    else:
        if secret == "":
            LabelSecretFeedback["text"] = "File empty"
        else:
            LabelSecretFeedback["text"] = "File loaded successfully."
        TextSecret.delete("1.0", "end")
        TextSecret.insert("1.0", secret)


# This function is invoked when the user clicks the button
# "Save secret to file".
# It tries to create or rewrite a textfile with the name
# specified in the corresponding entry field and to write
# the contents of the text field below into the file.
# Further, it tells the user whether the writing to the
# textfile succeeded.
def ButtonSecretSaveClick():
    ClearFeedbackLabels()
    secret = TextSecret.get("1.0", "end")[:-1]
    if secret == "":
        LabelSecretFeedback["text"] = "Nothing to save"
        return
    try:
        with open(PathSecret.get(), mode="wt", encoding="utf-8") as tf:
            if (tf.write(secret) != len(secret)):
                raise Exception
    except:
        LabelSecretFeedback["text"] = "An error occurred while saving to file."
    else:
        LabelSecretFeedback["text"] = "Secret saved successfully."


# This function is invoked by ButtonModeHideClick()
# after the secret was hidden successfully.
###### ENTER YOUR CODE HERE ######
def PrintImageComparison(ImageDataOffset):
    TextMode.delete("1.0", "end")
    TextMode.insert("1.0", ImageDataOffset)


# The following code lines try to display both
# bitmaps. They are not necessary for the program
# to work properly and may remain commented out.
##    try:
##        image = Image.open(PathImage.get())
##        width, height = image.size
##        ratio = min(LabelImageVirgin.winfo_width() / width,
##                    LabelImageVirgin.winfo_height() / height)
##        image = image.resize((math.floor(ratio * width),
##                              math.floor(ratio * height)))
##        image = ImageTk.PhotoImage(image)
##        LabelImageVirgin["image"] = image
##        LabelImageVirgin.image = image
##        image = Image.open(PathImage.get()[:-4] + "Hiding.bmp")
##        image = image.resize((math.floor(ratio * width),
##                              math.floor(ratio * height)))
##        image = ImageTk.PhotoImage(image)
##        LabelImageHiding["image"] = image
##        LabelImageHiding.image = image
##    except:
##        LabelModeFeedback["text"] = "An error occurred displaying the two images"


def Get_Bytearray_From_Image():
    with open(PathImage.get(), "rb") as image:
        return list(image.read())

bits = []
def DecimalToBinary(value):
    if value >= 1:
        DecimalToBinary(value // 2)
    bits.insert(value % 2)

def BinaryToDecimal(value):
    pass

offset = []
width = []
height = []

def Check_Image_Data(Image_As_List):
    if (Image_As_List[0] != 66 or Image_As_List[1] != 77):
        return "This is not an bmp file!";
    offset = Image_As_List[10:13]
    width = Image_As_List[18:21]
    height = Image_As_List[22:25]
    if Image_As_List[28] != 24:
        return "Wrong color depth!"
    if (1,2,3) in Image_As_List[30:33]:
        return "I have the highground!"
    if 0 not in Image_As_List[46:49]:
        return "Colortable is used!"
    return "";

def Change_Text_To_Binary(text):
    return format(ord(text), 'b') # not tested yet

# Convert one byte of image to 8 bit
# @return list
def Convert_Byte_To_Bit(Byte_On_Pixel):
    pass

def Change_Bit_From_Byte():
    pass

def Create_New_Image():
    pass

# This function is invoked when the user presses
# the button "Hide secret in image".
###### ENTER YOUR CODE HERE ######
def ButtonModeHideClick():
    ClearFeedbackLabels()
    imagearray = Get_Bytearray_From_Image()
    PrintImageComparison(imagearray)
    check = Check_Image_Data(imagearray)
    if check != "":
        LabelModeFeedback["text"] = check
        return
    for i in imagearray[max(offset):]:

    Convert_Byte_To_Bit()
    Change_Bit_From_Byte()
    Create_New_Image()
    PrintImageComparison()


# This function is invoked when the user presses
# the button "Disclose secret from image".
###### ENTER YOUR CODE HERE ######
def ButtonModeDiscloseClick():
    ClearFeedbackLabels()
    pass


# The window is divided into three frames.
FrameSecret = ttk.Frame(master=root)
FrameSecret["borderwidth"] = 5
FrameSecret["relief"] = "sunken"
FrameMode = ttk.Frame(master=root)
FrameMode["borderwidth"] = 5
FrameMode["relief"] = "sunken"
FrameImage = ttk.Frame(master=root)
FrameImage["borderwidth"] = 5
FrameImage["relief"] = "sunken"
FrameSecret.pack(side="left", fill="both", expand=True)
FrameMode.pack(side="left", fill="y")
FrameImage.pack(side="left", fill="both", expand=True)

# The labels, entries, buttons and text fields
# are defined and adjusted.
LabelSecretCaption = ttk.Label(master=FrameSecret, text="Secret text")
LabelSecretCaption.pack(side="top", pady=5)
PathSecret = tk.StringVar(value="./text.txt")
EntrySecret = ttk.Entry(master=FrameSecret, text=PathSecret)
EntrySecret.pack(side="top", padx=25, fill="x")
FrameSecretButtons = ttk.Frame(master=FrameSecret)
FrameSecretButtons.pack(side="top", padx=15, pady=5, fill="x")
ButtonSecretLoad = ttk.Button(master=FrameSecretButtons,
                              text="Load secret from file",
                              command=ButtonSecretLoadClick)
ButtonSecretSave = ttk.Button(master=FrameSecretButtons,
                              text="Save secret to file",
                              command=ButtonSecretSaveClick)
ButtonSecretLoad.pack(side="left", padx=10, fill="x", expand=True)
ButtonSecretSave.pack(side="right", padx=10, fill="x", expand=True)
LabelSecretFeedback = ttk.Label(master=FrameSecret, text="")
LabelSecretFeedback.pack(side="top", padx=25, pady=5, fill="x")
TextSecret = tk.Text(master=FrameSecret, width=10)
TextSecret.pack(side="bottom", fill="both", expand=True, padx=25, pady=10)

LabelModeCaption = ttk.Label(master=FrameMode, text="Mode")
LabelModeCaption.pack(side="top", pady=5)
PathImage = tk.StringVar(value="./image.bmp")
EntryImage = ttk.Entry(master=FrameMode, text=PathImage)
EntryImage.pack(side="top", padx=25, fill="x")
FrameImageButtons = ttk.Frame(master=FrameMode)
FrameImageButtons.pack(side="top", padx=15, pady=5, fill="x")
ButtonModeDisclose = ttk.Button(master=FrameImageButtons,
                                text="Disclose secret from image",
                                width=25,
                                command=ButtonModeDiscloseClick)
ButtonModeHide = ttk.Button(master=FrameImageButtons,
                            text="Hide secret in image",
                            width=ButtonModeDisclose.cget("width"),
                            command=ButtonModeHideClick)
ButtonModeDisclose.pack(side="right", padx=10, fill="x", expand=True)
ButtonModeHide.pack(side="left", padx=10, fill="x", expand=True)
LabelModeFeedback = ttk.Label(master=FrameMode, text="")
LabelModeFeedback.pack(side="top", padx=25, pady=5, fill="x")
TextMode = tk.Text(master=FrameMode, width=10)
TextMode.pack(side="bottom", fill="both", expand=True, padx=25, pady=10)

LabelImageHidingCaption = ttk.Label(master=FrameImage,
                                    text="Image containing the secret")
LabelImageHidingCaption.pack(side="top", pady=5)
LabelImageHiding = ttk.Label(master=FrameImage)
LabelImageHiding.pack(side="top", pady=5, fill="both", expand=True)
LabelImageVirginCaption = ttk.Label(master=FrameImage,
                                    text="Virgin image")
LabelImageVirginCaption.pack(side="top", pady=5)
LabelImageVirgin = ttk.Label(master=FrameImage)
LabelImageVirgin.pack(side="top", pady=5, fill="both", expand=True)

root.mainloop()
