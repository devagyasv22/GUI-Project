import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import numpy as np
from keras.models import load_model

# Load the saved CNN model
model = load_model(r'C:\Users\NEXSTGO\OneDrive\Desktop\c language\1\final_defects.ipynb')

def open_images():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        for file_path in file_paths:
            image = Image.open(file_path)
            image.thumbnail((250, 250))
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(image_frame, image=photo, bg='white')
            label.image = photo
            label.pack(padx=10, pady=10, side=tk.LEFT)
            images.append(image)
            file_names.append(os.path.basename(file_path))
        update_loaded_images_label()

def check_defects():
    if images:
        image = images.pop(0)
        file_name = file_names.pop(0)
        
        image = image.resize((224, 224))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')

        image = np.array(image)
        image = image.reshape(1, 224, 224, 3)
        image = image / 255.0
        
        res = model.predict([image])[0]
        predicted_digit = np.argmax(res)
        defect_names = [
            "Blister", "Dezincification", "Dislocations", "Gas holes", "Inclusions",
            "Incomplete grain recrystallization", "Orange Peel", "Stress corrosion crack"
        ]
        predicted_defect = defect_names[predicted_digit]
        show_defect(file_name, predicted_defect)
        display_prediction(file_name, predicted_defect)

def show_defect(file_name, predicted_defect):
    defect_label.config(text=f"Image: {len(images) + 1} - Predicted Defect: {predicted_defect}", fg='green')

def update_loaded_images_label():
    loaded_label.config(text="Loaded Images: {}".format(len(images)), fg='blue')

def display_prediction(file_name, predicted_defect):
    for widget in image_frame.winfo_children():
        if widget.winfo_name() == file_name:
            tk.Label(widget, text=f"Defect: {predicted_defect}", bg='white', fg='red').pack()

def reset():
    global images, file_names
    images = []
    file_names = []
    for widget in image_frame.winfo_children():
        widget.destroy()
    update_loaded_images_label()
    defect_label.config(text="Defect Prediction Results")

# Tkinter setup
root = tk.Tk()
root.title("Defects Image Viewer")
root.geometry('800x600')
root.configure(bg='light grey')

# Style configuration
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10), padding=10)
style.configure('TLabel', font=('Helvetica', 12))

# Frame for buttons
button_frame = tk.Frame(root, bg='light grey')
button_frame.pack(pady=20)

open_button = tk.Button(button_frame, text="Open Images", command=open_images, bg='light blue', fg='black', font=('Helvetica', 10, 'bold'))
open_button.pack(side=tk.LEFT, padx=10)

check_button = tk.Button(button_frame, text='Check Type of Defects', command=check_defects, bg='light green', fg='black', font=('Helvetica', 10, 'bold'))
check_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(button_frame, text='Reset', command=reset, bg='light coral', fg='black', font=('Helvetica', 10, 'bold'))
reset_button.pack(side=tk.LEFT, padx=10)

image_frame = tk.Frame(root, bg='white', bd=2, relief=tk.SUNKEN)
image_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

defect_label = tk.Label(root, text="Defect Prediction Results", font=("Helvetica", 14, "bold"), bg='light grey')
defect_label.pack(pady=10)

loaded_label = tk.Label(root, text="Loaded Images: 0", font=("Helvetica", 12), bg='light grey', fg='blue')
loaded_label.pack(pady=10)

images = []
file_names = []

root.mainloop()
