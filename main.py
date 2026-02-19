import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# 📁 File categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3", ".wav"]
}


def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return "Others"


def organize_folder(path):
    if not os.path.exists(path):
        messagebox.showerror("Error", "Folder does not exist!")
        return

    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            if os.path.isfile(item_path):
                name, extension = os.path.splitext(item)
                category = get_category(extension)

                category_folder = os.path.join(path, category)

                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)

                destination = os.path.join(category_folder, item)

                # Prevent overwriting
                if os.path.exists(destination):
                    counter = 1
                    while os.path.exists(destination):
                        new_name = f"{name}_{counter}{extension}"
                        destination = os.path.join(category_folder, new_name)
                        counter += 1

                shutil.move(item_path, destination)

        messagebox.showinfo("Success", "Files organized successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        organize_folder(folder_selected)


# 🎨 GUI Setup
root = tk.Tk()
root.title("File Organizer")
root.geometry("400x200")
root.resizable(False, False)

label = tk.Label(root, text="Select a folder to organize", font=("Arial", 14))
label.pack(pady=20)

browse_button = tk.Button(root, text="Browse Folder", font=("Arial", 12), command=browse_folder)
browse_button.pack(pady=10)

root.mainloop()
