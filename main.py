import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import shutil

# Tkinter Settings
root = tk.Tk()
root.title("Data Cleaning Tool by Mustafa Mert Çolak")
root.resizable(False, False)
root.geometry('1280x764')
root.iconphoto(False, tk.PhotoImage(file='images/icon.png'))
root.iconname()

# Global variables
current_input_folder = None
current_output_folder = None
current_delete_folder = None
current_image_index = 0
image_files = []

# Tkinter Methods
def select_folder_method():
    return filedialog.askdirectory()

def create_popup():
    # Input Window Settings
    input_window = tk.Toplevel()
    input_window.geometry('800x600')
    input_window.title('Select Folders')

    def set_input_folder():
        input_folder = select_folder_method()
        input_label.config(text=f"Input Folder: {input_folder}")

    def set_output_folder():
        output_folder = select_folder_method()
        output_label.config(text=f"Output Folder: {output_folder}")

    def set_delete_folder():
        delete_folder = select_folder_method()
        delete_label.config(text=f'Delete Folder: {delete_folder}')

    def submit_folders():
        global current_input_folder, current_output_folder, current_delete_folder
        current_input_folder = input_label.cget("text").replace("Input Folder: ", "")
        current_output_folder = output_label.cget("text").replace("Output Folder: ", "")
        current_delete_folder = delete_label.cget("text").replace("Delete Folder: ", "")
        list_files(current_input_folder)
        list_output_files(current_output_folder)
        print(f"Input Folder: {current_input_folder}")
        print(f"Output Folder: {current_output_folder}")
        print(f"Delete Folder: {current_delete_folder}")
        input_window.destroy()

    input_button = tk.Button(input_window, text='Select Input Folder', command=set_input_folder, pady=20, padx=20)
    input_button.pack(pady=20)

    output_button = tk.Button(input_window, text='Select Output Folder', command=set_output_folder, pady=20, padx=20)
    output_button.pack(pady=20)

    delete_button = tk.Button(input_window, text='Select Delete Folder', command=set_delete_folder, pady=20, padx=20)
    delete_button.pack(pady=20)

    input_label = tk.Label(input_window, text="Input Folder: Not Selected", pady=10)
    input_label.pack()

    output_label = tk.Label(input_window, text="Output Folder: Not Selected", pady=10)
    output_label.pack()

    delete_label = tk.Label(input_window, text="Delete Folder: Not Selected", pady=10)
    delete_label.pack()

    submit_button = tk.Button(input_window, text='Submit', command=submit_folders, pady=20, padx=20)
    submit_button.pack(pady=20)

def list_files(folder_path):
    global image_files
    file_list.delete(0, tk.END)  # Clear the listbox
    if folder_path and os.path.isdir(folder_path):
        image_files = [f for f in os.listdir(folder_path) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        for file in image_files:
            file_list.insert(tk.END, file)

def list_output_files(folder_path):
    output_file_list.delete(0, tk.END)  # Clear the output listbox
    if folder_path and os.path.isdir(folder_path):
        output_files = [f for f in os.listdir(folder_path) if
                        f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.txt'))]
        for file in output_files:
            output_file_list.insert(tk.END, file)

def list_delete_files(folder_path):
    delete_file_list.delete(0, tk.END)  # Clear the delete listbox
    if folder_path and os.path.isdir(folder_path):
        delete_files = [f for f in os.listdir(folder_path) if
                        f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.txt'))]
        for file in delete_files:
            delete_file_list.insert(tk.END, file)

def display_image(event=None):
    global current_image_index
    if event:
        selected_file = file_list.get(file_list.curselection())
        current_image_index = image_files.index(selected_file)
    if image_files:
        file_path = os.path.join(current_input_folder, image_files[current_image_index])
        image = Image.open(file_path)
        image = image.resize((800, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
        image_name_label.config(text=image_files[current_image_index])
    else:
        image_label.config(image='')
        image_name_label.config(text='No images left')

def display_output_image(event=None):
    global current_image_index
    if event:
        selected_file = output_file_list.get(output_file_list.curselection())
        current_image_index = output_file_list.curselection()[0]  # Get the selected index
        file_path = os.path.join(current_output_folder, selected_file)
        image = Image.open(file_path)
        image = image.resize((800, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
        image_name_label.config(text=selected_file)

def next_image(event=None):
    global current_image_index
    if current_image_index < len(image_files) - 1:
        current_image_index += 1
        display_image()

def prev_image(event=None):
    global current_image_index
    if current_image_index > 0:
        current_image_index -= 1
        display_image()

def move_image(event=None):
    global current_image_index
    if image_files and current_input_folder and current_output_folder:
        current_file = image_files[current_image_index]
        src_image = os.path.join(current_input_folder, current_file)
        dst_image = os.path.join(current_output_folder, current_file)

        # Move the image file
        shutil.move(src_image, dst_image)

        # Check for a corresponding .txt file and move it if it exists
        txt_file = os.path.splitext(current_file)[0] + '.txt'
        src_txt = os.path.join(current_input_folder, txt_file)
        dst_txt = os.path.join(current_output_folder, txt_file)
        if os.path.exists(src_txt):
            shutil.move(src_txt, dst_txt)

        image_files.pop(current_image_index)
        if current_image_index >= len(image_files):
            current_image_index = len(image_files) - 1
        display_image()
        list_output_files(current_output_folder)
        list_files(current_input_folder)

def delete_image(event=None):
    global current_image_index
    if image_files and current_input_folder and current_delete_folder:
        current_file = image_files[current_image_index]
        src_image = os.path.join(current_input_folder, current_file)
        dst_image = os.path.join(current_delete_folder, current_file)

        # Move the image file to the delete folder
        shutil.move(src_image, dst_image)

        # Check for a corresponding .txt file and move it if it exists
        txt_file = os.path.splitext(current_file)[0] + '.txt'
        src_txt = os.path.join(current_input_folder, txt_file)
        dst_txt = os.path.join(current_delete_folder, txt_file)
        if os.path.exists(src_txt):
            shutil.move(src_txt, dst_txt)

        image_files.pop(current_image_index)
        if current_image_index >= len(image_files):
            current_image_index = len(image_files) - 1
        display_image()
        list_files(current_input_folder)
        list_output_files(current_output_folder)
        list_delete_files(current_delete_folder)

# Create a frame on the left side of the root window
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Create a Label to display "Input Folder" at the top of the left listbox
input_folder_label = tk.Label(left_frame, text="Input Folder", pady=10)
input_folder_label.pack()

# Create a Listbox to display the files
file_list = tk.Listbox(left_frame, width=25, height=20)
file_list.pack(side=tk.LEFT, fill=tk.Y)

# Create a frame for the output and delete folder files
output_delete_frame = tk.Frame(root)
output_delete_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a Label to display "Output Folder" at the top of the right listbox
output_folder_label = tk.Label(output_delete_frame, text="Output Folder", pady=10)
output_folder_label.pack()

# Create a Listbox to display the output folder files
output_file_list = tk.Listbox(output_delete_frame, width=25, height=20)
output_file_list.pack(side=tk.TOP, fill=tk.Y)


# Create a Label to display "Delete Folder" at the bottom
delete_folder_label = tk.Label(output_delete_frame, text="Delete Folder", pady=10)
delete_folder_label.pack()

# Create a Listbox to display the delete folder files
delete_file_list = tk.Listbox(output_delete_frame, width=25, height=20)
delete_file_list.pack(side=tk.TOP, fill=tk.Y)

# Bind the Listbox selection event to display the image
file_list.bind('<<ListboxSelect>>', display_image)

# Bind the output listbox selection event to display the output image
output_file_list.bind('<<ListboxSelect>>', display_output_image)

# Create a frame for the image and navigation buttons
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a Label to display the image
image_label = tk.Label(right_frame)
image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a Label to display the image name
image_name_label = tk.Label(right_frame, text="", pady=10)
image_name_label.pack(side=tk.TOP)

# Create navigation buttons
prev_button = tk.Button(right_frame, text="Previous", command=prev_image, padx=50)
prev_button.pack(side=tk.LEFT, padx=10, pady=10)

move_button = tk.Button(right_frame, text="Move", command=move_image, padx=50)
move_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = tk.Button(right_frame, text="Delete", command=delete_image, padx=50)
delete_button.pack(side=tk.LEFT, padx=10, pady=10)

next_button = tk.Button(right_frame, text="Next", command=next_image, padx=50)
next_button.pack(side=tk.LEFT, padx=10, pady=10)

# Bind arrow keys to navigate images
root.bind('<Right>', next_image)
root.bind('<Left>', prev_image)
root.bind('<space>', move_image)
root.bind('<BackSpace>', delete_image)

# Create Window
create_popup()
root.mainloop()
