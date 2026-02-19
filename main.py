import os
import shutil
import streamlit as st
from tempfile import TemporaryDirectory
import zipfile

# --- File categories ---
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
    """Organize all files in the given folder path by category."""
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

            # Handle duplicate filenames
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
st.title("📂 File Organizer Web App (Drag & Drop)")

uploaded_files = st.file_uploader(
    "Drag and drop your files here (you can select multiple)",
    type=None,
    accept_multiple_files=True
)

if uploaded_files:
    # Use a temporary folder to store uploaded files
    with TemporaryDirectory() as temp_dir:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        # Organize files
        moved = organize_folder(temp_dir)
        st.success(f"✅ Successfully organized {moved} files!")

        # Show organized files by category
        for category in FILE_CATEGORIES.keys():
            category_path = os.path.join(temp_dir, category)
            if os.path.exists(category_path):
                st.write(f"**{category}**:")
                st.write(os.listdir(category_path))

        # Others
        others_path = os.path.join(temp_dir, "Others")
        if os.path.exists(others_path):
            st.write("**Others**:")
            st.write(os.listdir(others_path))

        # --- Zip all organized files for download ---
        zip_path = os.path.join(temp_dir, "organized_files.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file != "organized_files.zip":  # avoid including the zip in itself
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)

        # Download button
        with open(zip_path, "rb") as f:
            st.download_button(
                label="📥 Download Organized Files",
                data=f,
                file_name="organized_files.zip",
                mime="application/zip"
            )
