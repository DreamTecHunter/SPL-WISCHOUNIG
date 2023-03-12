# tkinter provides GUI objects and commands
import tkinter as tk
import tkinter.ttk as ttk
import csv
from ast import literal_eval
# math provides some functions (ceil, floor)
import math
# Python Imaging Library (PIL) provides commands
# to comfortably open and save bitmap files
from PIL import Image, ImageTk

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
    pass


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

# This function is invoked when the user presses
# the button "Hide secret in image".
###### ENTER YOUR CODE HERE ######
def ButtonModeHideClick():
    ClearFeedbackLabels()
    try:
        file = open(PathImage.get(), "rb")
        file_content = list(file.read())
    except:
        LabelModeFeedback["text"] = "Could not read the specific file or/and hasn't been converted to binary!"
    # bitmapfileheader 0:13
    if file_content[0] != 66 and file_content[1] != 77:
        LabelModeFeedback["text"] = "File is not a .bmp"
        return
    bf_off_bits = file_content[10:14]
    # bitmapinfoheader 14:39
    width = file_content[18:22]
    height = file_content[22:26]
    if file_content[28] != 24 or file_content[29] != 24:
        LabelModeFeedback["text"] = "Bitmap doesn't have the needed color depth. color depth 24 is needed."
        return
    if file_content[30] != 0:  # 30:33
        LabelModeFeedback["text"] = "Bitmap isn't allowed to be compressed."
        return
    if file_content[46] != 0:  # 46:49
        LabelModeFeedback["text"] = "Bitmap isn't allowed to have a colortable."  #
        return
    # bitMapInfoBody 54: -
    secret = TextSecret.get('1.0', 'end')[:-1]  # get secret text
    if len(file_content) - 54 < len(secret) * 8:  # check length from secret and bitmap
        LabelModeFeedback["text"] = "Secret hasn't enough space in the bitmap! Bitmap is " \
                                    + str(len(file_content) - 54 - len(secret) * 8) + " bit/s to short"
        return
    fits = False
    if len(file_content) - 54 == len(secret) * 8:
        fits = True
    elif len(file_content) - 54 < len(secret) * 8 + 8:
        LabelModeFeedback["text"] = \
            "Secret hasn't enough space including the 8-end-characters in the bitmap! Bitmap is " \
            + str(len(file_content) - 54 - len(secret) * 8 - 8) + " bit/s to short"
        return
    new_list = []
    # iterate secret to convert to a list of the bits
    for item in list(secret):  # iterate secret letter for letter
        item_binary = list(bin(ord(item)).replace("0b", ""))  # convert letter to binary
        # when binary-letter has less than 8 bits, filling up to 8 bits
        [item_binary.insert(0, '0') for i in range(0, 8 - len(item_binary))]
        [new_list.append(ib) for ib in reversed(item_binary)]  # add bits to list
        blank = 0
        width_dez_value = 0
        for g in range(len(width)):
            width_dez_value += width[g] * 255 ** g
        if not fits:
            new_list = new_list + ['0'] * 8
    for i in range(len(new_list)):
        b = False
        fc = ['0'] * 8
        temp = list(reversed(list(bin(file_content[54 + i + blank]).replace("0b", ""))))
        for j in range(len(temp)):
            fc[j] = temp[j]
        fc = list(reversed(fc))
        fc[-1] = new_list[i]
        n = 0
        for j in range(len(fc)):
            n = n + int(list(reversed(fc))[j]) * 2 ** j
        file_content[54 + i + blank] = n
    try:
        new_file_name_list = file.name.split(".")
        new_file = open("" + new_file_name_list[0] + "Hiding." + new_file_name_list[1], "wb")
        new_file.write(bytes(file_content))
    except:
        LabelModeFeedback["text"] = \
            "" + new_file_name_list[0] + "Hiding." + new_file_name_list[1] + " cannot be created."


# This function is invoked when the user presses
# the button "Disclose secret from image".
###### ENTER YOUR CODE HERE ######
def ButtonModeDiscloseClick():
    ClearFeedbackLabels()
    try:
        file = open("GalaxienHiding.bmp", "rb")
        data = list(file.read())
    except:
        LabelModeFeedback["text"] = "Could not open file or/and read it!"
        if data[0] != 66 and data[1] != 77:
            LabelModeFeedback["text"] = "The opened file is not a bmp file!"

        print(data[2:10], "ignoring those 4x2 bytes")
        bfOffBits = data[10:14]
        print(data[14:18, "ignoring those 4 bytes"])
        bi_width = data[18:22]
        print(bi_width)
        bi_height = data[22:26]
        print(bi_height)
        print(data[26:28], "ignoring biPlanes")
        if data[28] != 24 or data[29] != 24:
            LabelModeFeedback["text"] = "the bmp file is not a 24 bit bmp file, pls resave it!"
            pass
        if data[30] == 0:  # 30:33
            print("biCompression is ok")
        else:
            LabelModeFeedback["text"] = "Compression detected, we are not allowing compression!"
        print(data[34:46])
        if data[46] == 0:  # 46:49
            print("biClrUsed is ok")
        else:
            LabelModeFeedback["text"] = "Colored tables detected, we are not allowing colored tables!"
        print(data[50:54])
        # bitMapInfoBody

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
