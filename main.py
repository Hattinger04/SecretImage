# tkinter provides GUI objects and commands
import tkinter as tk
import tkinter.ttk as ttk
# math provides some functions (ceil, floor)
import math
# Python Imaging Library (PIL) provides commands
# to comfortably open and save bitmap files
from PIL import Image, ImageTk
import io
import numpy as np

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

# List of Bytes from Image
def Get_Bytearray_From_Image():
    with open(PathImage.get(), "rb") as image:
        return list(image.read())


bits = []


def DecimalToBinary(value):
    if value >= 1:
        DecimalToBinary(value // 2)
    bits.append(value % 2)


def BinaryToDecimal(value):
    return int(value)


offset = []
width = []
height = []


# Validation
def Check_Image_Data(Image_As_List):
    global offset, width, height
    if (Image_As_List[0] != 66 or Image_As_List[1] != 77):
        return "This is not an bmp file!";
    offset = Image_As_List[10:13]
    width = Image_As_List[18:21]
    height = Image_As_List[22:25]
    if Image_As_List[28] != 24:
        return "Wrong color depth!"
    if (1, 2, 3) in Image_As_List[30:33]:
        return "I have the highground!"
    if 0 not in Image_As_List[46:49]:
        return "Colortable is used!"
    return "";


# Inputtext into List of Binarynumbers
def Change_Text_To_Binary(text):
    binary = []
    for s in text:
        binary.append(Change_Char_To_Binary(s))
    return binary


def Change_Char_To_Binary(char):
    binary = bin(ord(char))[2:]
    # need all 8 digits
    for i in range(len(binary), 8):
        binary = "0" + binary
    return binary


def Change_Last_Bit(byte, new_bit):
    global bits
    bits = []
    DecimalToBinary(byte)
    bits[len(bits) - 1] = new_bit
    return BinaryToDecimal(''.join(str(e) for e in bits))


def Create_New_Image(imagearray):
    with open(PathImage.get()[:len(PathImage.get()) - 4] + "Hiding" + PathImage.get()[len(PathImage.get()) - 4:], "wb+") as image:
        image.write(bytes(imagearray))


def Get_Correct_Value(value):
    real_value = 0
    mulitplicator = 1
    for i in range(0, 2):
        real_value += (value[i] * mulitplicator)
        mulitplicator *= 256
    return real_value


def InsertBitsInImage(imagearray, correct_offset, correct_width, correct_height, binary_bits):
    counter_image = 0
    counter_word = 0
    for byte in imagearray[correct_offset:correct_offset + len(binary_bits) + correct_height]:
        if counter_word % (correct_width * (3 * (4 - correct_width))) == 0 and counter_image != 0:
            counter_image += (3 * (4 - correct_width))
        imagearray[correct_offset + counter_image] = int(
                str(Change_Last_Bit(imagearray[correct_offset + counter_image], binary_bits[counter_word])), 2)
        counter_image += 1
        counter_word += 1
        if len(binary_bits) == counter_word:
            #imagearray.insert(correct_offset + counter_image, 0)
            break

# This function is invoked when the user presses
# the button "Hide secret in image".
###### ENTER YOUR CODE HERE ######
def ButtonModeHideClick():
    global offset, width, height
    ClearFeedbackLabels()
    imagearray = Get_Bytearray_From_Image()  # list of image information
    print(imagearray)
    PrintImageComparison(imagearray)  # print to textfield

    check = Check_Image_Data(imagearray)  # validation for image information
    if check != "":
        LabelModeFeedback["text"] = check  # Return Error if one exists
        return

    binary_word = Change_Text_To_Binary("äl")  # list in list for change
    binary_bits = []
    for i in binary_word:
        for s in i:
            binary_bits.append(s)

    correct_offset = Get_Correct_Value(offset)
    correct_width = Get_Correct_Value(width)
    correct_height = Get_Correct_Value(height)

    if len(binary_bits) > len(imagearray[correct_offset:]) - (correct_height * 3):
        LabelModeFeedback["text"] = "Text too long for this image!"
        return
    InsertBitsInImage(imagearray, correct_offset, correct_width, correct_height, binary_bits)
    Create_New_Image(imagearray)
    with open("./img/miniHiding.bmp", "rb") as image:
        print(list(image.read()))
    PrintImageComparison(imagearray)


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
PathImage = tk.StringVar(value="./img/mini.bmp")
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
