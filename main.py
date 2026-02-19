import os
import shutil
import streamlit as st

# File categories
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
    moved_files = 0

    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isfile(item_path):
            name, extension = os.path.splitext(item)
            category = get_category(extension)

            category_folder = os.path.join(path, category)

            if not os.path.exists(category_folder):
                os.makedirs(category_folder)

            destination = os.path.join(category_folder, item)

            if os.path.exists(destination):
                counter = 1
                while os.path.exists(destination):
                    new_name = f"{name}_{counter}{extension}"
                    destination = os.path.join(category_folder, new_name)
                    counter += 1

            shutil.move(item_path, destination)
            moved_files += 1

    return moved_files


# --- Streamlit UI ---
st.title("📂 File Organizer Web App")

folder_path = st.text_input("Enter folder path to organize:")

if st.button("Organize Files"):
    if os.path.exists(folder_path):
        moved = organize_folder(folder_path)
        st.success(f"✅ Successfully organized {moved} files!")
    else:
        st.error("❌ Folder does not exist.")
