import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from PIL import Image, ImageTk
from signature import match

# Match Threshold
THRESHOLD = 85

def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("test")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)  # make sure the directory exists
            img_name = "./temp/test_img1.png" if sign == 1 else "./temp/test_img2.png"
            print('imwrite=', cv2.imwrite(filename=img_name, img=frame))
            print("{} written!".format(img_name))
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1):
    filename = os.getcwd() + ('\\temp\\test_img1.png' if sign == 1 else '\\temp\\test_img2.png')
    res = messagebox.askquestion('Click Picture', 'Press Space Bar to click picture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign)
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)

def compare_images(path1, path2):
    similarity_value = match(path1, path2)
    if similarity_value >= THRESHOLD:
        messagebox.showinfo('Result', f'Signatures match! Similarity: {similarity_value:.2f}%')
    else:
        messagebox.showinfo('Result', f'Signatures do not match. Similarity: {similarity_value:.2f}%')

# Create main window
root = tk.Tk()
root.title("Signature Matcher")
root.geometry('500x400')

# Add background image
background_image = Image.open("background.jpg")  # Make sure this path is correct
background_image = background_image.resize((500, 400), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=500, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Styling
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 10)
button_font = ("Helvetica", 10, "bold")
button_bg = "#4CAF50"
button_fg = "white"

# Padding values
padx = 10
pady = 5

# Add widgets on top of the canvas
image1_path_label = tk.Label(root, text="Image 1 Path:", font=label_font, bg='#f0f0f0')
canvas.create_window(70 - padx, 50, window=image1_path_label)
image1_path_entry = tk.Entry(root, width=30, font=entry_font)
canvas.create_window(250 - padx, 50, window=image1_path_entry)
image1_browse_button = tk.Button(root, text="Browse", command=lambda: browsefunc(image1_path_entry),
                                 font=button_font, bg=button_bg, fg=button_fg)
canvas.create_window(420 - padx, 50, window=image1_browse_button)

image2_path_label = tk.Label(root, text="Image 2 Path:", font=label_font, bg='#f0f0f0')
canvas.create_window(70 - padx, 100, window=image2_path_label)
image2_path_entry = tk.Entry(root, width=30, font=entry_font)
canvas.create_window(250 - padx, 100, window=image2_path_entry)
image2_browse_button = tk.Button(root, text="Browse", command=lambda: browsefunc(image2_path_entry),
                                 font=button_font, bg=button_bg, fg=button_fg)
canvas.create_window(420 - padx, 100, window=image2_browse_button)

capture_button1 = tk.Button(root, text="Capture Image 1", command=lambda: captureImage(image1_path_entry, 1),
                            font=button_font, bg=button_bg, fg=button_fg)
canvas.create_window(150, 150 + pady, window=capture_button1)
capture_button2 = tk.Button(root, text="Capture Image 2", command=lambda: captureImage(image2_path_entry, 2),
                            font=button_font, bg=button_bg, fg=button_fg)
canvas.create_window(300, 150 + pady, window=capture_button2)

compare_button = tk.Button(root, text="Compare Signatures", command=lambda: compare_images(
    path1=image1_path_entry.get(), path2=image2_path_entry.get()),
    font=button_font, bg=button_bg, fg=button_fg)
canvas.create_window(230, 200 + pady * 2, window=compare_button)

root.mainloop()
