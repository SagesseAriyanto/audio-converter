import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import platform

# Store path of uploaded PDF
pdf_path = None

window = tk.Tk()
window.title("PDF Audio")
window.minsize(600, 500)

# Function to handle PDF upload
def upload_pdf():
    global pdf_path
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Select a PDF file"
    )
    if file_path:
        pdf_path = file_path
        # Update label and show convert button
        pdf_label.config(text=os.path.basename(pdf_path))
        pdf_label.pack(pady=7)
        convert_btn.pack(pady=(60,10))

label = tk.Label(
    window,
    text="Welcome to PDF Audio Application",
    fg="blue",
    font=("Arial", 16, "bold"),
)
label.pack(pady=20)

upload = tk.Button(window, text="Upload PDF", command=upload_pdf)
upload.pack(pady=10)

# PDF file label after upload
pdf_label = tk.Label(
    window,
    text=""
)
convert_btn = tk.Button(window, text="Convert PDF to Audio", width=25)


window.mainloop()
