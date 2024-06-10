
import os
import pickle
import tkinter as tk
from tkinter import messagebox
import face_recognition


def get_button(window, text, color, command, fg='white'):
    """Create a button widget."""
    button = tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=20,
        font=('Helvetica bold', 20)
    )
    return button


def get_img_label(window):
    """Create an image label widget."""
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    """Create a text label widget."""
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    """Create a text entry widget."""
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    """Show a message box."""
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    """Recognize a face using face_recognition library."""
    # Check if any face is detected in the image
    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'

    embeddings_unknown = embeddings_unknown[0]

    # Check if the database directory exists
    if not os.path.exists(db_path):
        return 'database_not_found'

    # Iterate through files in the database directory
    db_dir = sorted(os.listdir(db_path))
    match = False
    j = 0

    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        # Load embeddings from the database file
        try:
            with open(path_, 'rb') as file:
                embeddings = pickle.load(file)
        except (IOError, pickle.UnpicklingError) as e:
            print(f"Error loading file: {path_}: {e}")
            j += 1
            continue

        # Compare faces
        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]  # Extract the name from the filename
    else:
        return 'unknown_person'


