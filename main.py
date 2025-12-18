import tkinter as tk
from tkinter import filedialog
import os
import shutil
from PIL import Image, ImageTk

# Store path of uploaded PDF
pdf_path = None

window = tk.Tk()
window.title("PDF Audio")
window.minsize(600, 500)
window.resizable(False, False)

# Function to handle PDF upload
def upload_pdf():
    global pdf_path
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Select a PDF file"
    )
    if file_path:
        pdf_path = file_path
        pdf_label.config(text=os.path.basename(pdf_path))

        # Display PDF icon
        pdf_icon = Image.open("./Assets/pdf.ico").resize((25, 25))
        pdf_icon_photo = ImageTk.PhotoImage(pdf_icon)
        pdf_canvas = tk.Canvas(pdf_frame, width=25, height=25)
        pdf_canvas.pack(side="left")
        pdf_canvas.create_image(12.5, 12.5, image=pdf_icon_photo)
        pdf_canvas.image = pdf_icon_photo                               # keep a global reference 

        # Display PDF filename
        pdf_label.pack(side="left", padx=5)

# Function to save PDF for review
def save_pdf():
    if pdf_path:
        filename = os.path.basename(pdf_path)
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=filename,
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF for Review"
        )
    if save_path:
        shutil.copy(pdf_path, save_path)            # copy the PDF to the selected location


# Title Label
title = tk.Label(
    window,
    text="Welcome to PDF Audio Application",
    fg="blue",
    font=("Arial", 16, "bold"),
)
title.pack(pady=20)

# Upload pdf Button
upload = tk.Button(window, text="Upload PDF", command=upload_pdf)
upload.pack(pady=10)

# PDF frame for icon and label
pdf_frame = tk.Frame(window)
pdf_frame.pack(pady=(10, 60))
pdf_label = tk.Label(pdf_frame, text="", cursor="hand2", font=("Arial", 10, "bold"))
pdf_label.bind("<Button-1>", lambda e: save_pdf())          # make label clickable to save PDF for review


convert_btn = tk.Button(window, text="Convert PDF to Audio", width=25)


window.mainloop()
