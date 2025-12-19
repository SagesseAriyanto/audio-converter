import tkinter as tk
from tkinter import filedialog
import os
import shutil
from PIL import Image, ImageTk

pdf_path = None     # Store path of uploaded PDF

window = tk.Tk()
window_bg = "#F5F3FF"
window.config(bg=window_bg)

window.title("PDF Audio")
window.minsize(600, 500)
window.resizable(False, False)

# Function to handle PDF upload
def upload_pdf():
    global pdf_path, condition
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")],
        title="Select a PDF file"
    )
    if file_path:
        pdf_path = file_path

        # Reset previoud display
        text_frame.pack_forget()
        control_frame.pack_forget()
        
        # Reset play/pause button text
        pause_play_button.config(image=play_icon)


        pdf_label.config(text=os.path.basename(pdf_path))

        
        # Display PDF icon and filename
        pdf_canvas.pack(side="left")
        pdf_label.pack(side="left", padx=5)
        convert_btn.pack()

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

# Function to find and resize image
def find_img(loc, size):
    img = Image.open(loc).resize(size)
    return ImageTk.PhotoImage(img)

# TODO: Function to rewind or forward audio
def rewind(direction):
    pass

# Function to play or pause audio
def play_pause():
    if pause_play_button.image == play_icon:
        pause_play_button.config(image=pause_icon)
        pause_play_button.image = pause_icon
        # TODO: pause audio playback
    else:
        pause_play_button.config(image=play_icon)
        pause_play_button.image = play_icon
        # TODO: resume audio playback


# Function to generate navigation icons for audio playback
def generate_icons():
    convert_btn.pack_forget()
    control_frame.pack()
    back_button.pack(side="left", padx=13, pady=5)
    pause_play_button.pack(side="left")
    forward_button.pack(side="left", padx=13, pady=5)


# Function to extract text from PDF
def get_text_from_pdf(path):
    pass


# Function to convert PDF text to audio
def convert_audio():
    text_frame.pack(pady=10)
    generate_icons()
    text_area.pack(
        padx=5,
        pady=5,
        fill="both",
    )


# Title Label
title = tk.Label(
    window,
    text="Welcome to PDF Audio Application",
    fg="blue",
    font=("Arial", 16, "bold"),
)
title.pack(pady=20)

# Upload pdf Button
upload_icon = find_img("./Assets/upload.png", (50, 50))
upload = tk.Button(window, image=upload_icon, command=upload_pdf, bd=0)
upload.pack(pady=10)

# Main frame for icon, controls, and text
main_frame = tk.Frame(window)
main_frame.pack()

# PDF frame for icon and filename
pdf_frame = tk.Frame(main_frame)
pdf_frame.pack(pady=(5, 60))

# Save PDF icon and label
pdf_icon_photo = find_img("./Assets/pdf.ico", (25, 25))
pdf_canvas = tk.Canvas(pdf_frame, width=25, height=25)
pdf_canvas.create_image(12.5, 12.5, image=pdf_icon_photo)

pdf_label = tk.Label(pdf_frame, cursor="hand2", font=("Arial", 10, "bold"))
pdf_label.bind("<Button-1>", lambda e: save_pdf())                                       # make label clickable to save PDF for review


# Control frame for backward, pause/play, and forward buttons
control_frame = tk.Frame(main_frame)

# Load navigation icons
back_icon = find_img("./Assets/rewind.png", (30, 30))
forward_icon = find_img("./Assets/fastforward.png", (30, 30))

back_button = tk.Button(
    control_frame,
    image=back_icon,
    command=rewind("back"),
    bd=0,
)

play_icon = find_img("./Assets/play.png", (35, 35))
pause_icon = find_img("./Assets/pause.png", (35, 35))
pause_play_button = tk.Button(
    control_frame,
    image=play_icon,
    bd=0,
    command=play_pause,
)
pause_play_button.image = play_icon  # Keep reference to the image

forward_button = tk.Button(
    control_frame,
    image=forward_icon,
    command=rewind("forward"),
    bd=0,
)


# Convert pdf text audio
convert_btn = tk.Button(window, text="Convert PDF to Audio", width=25, command=convert_audio)

# Text area to display pdf content
text_frame = tk.Frame(window)
text_area = tk.Text(
    text_frame,
    height=10,
    width=65,
    wrap="word",            # wrap text by word within the text area
    state="normal",
    spacing2=5,
    spacing3=15,
)


# Update all frames and labels background color
main_frame.config(bg=window_bg)
pdf_frame.config(bg=window_bg)
control_frame.config(bg=window_bg)
text_frame.config(bg=window_bg)
text_area.config(bg="#FEFCFF", fg="#3A3A3A")
title.config(bg=window_bg)
pdf_label.config(bg=window_bg)

# Update buttons background color
upload.config(bg=window_bg, activebackground=window_bg)
convert_btn.config(bg=window_bg, activebackground=window_bg)
back_button.config(bg=window_bg, activebackground=window_bg)
forward_button.config(bg=window_bg, activebackground=window_bg)
pause_play_button.config(bg=window_bg, activebackground=window_bg)

window.mainloop()
