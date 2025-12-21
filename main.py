import tkinter as tk
from tkinter import filedialog, ttk
import os
import shutil
from PIL import Image, ImageTk
import pdfplumber
import pyttsx3
import threading

pdf_path = None                     # Store path of uploaded PDF
extracted_text = ""                 # Store extracted PDF text

window = tk.Tk()
window_bg = "#F5F3FF"
window.config(bg=window_bg)
window.iconbitmap("./Assets/audio.ico")
window.title("DocAudio - PDF to Audio")
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

        # Update PDF filename label
        pdf_label.config(text=os.path.basename(pdf_path))
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


# Function to play or pause audio
def play_stop():
    global extracted_text
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 172)
    engine.setProperty("volume", 0.9)

    # If icon is play, start playing audio
    if pause_play_button.image == play_icon:
        pause_play_button.config(image=stop_icon)
        pause_play_button.image = stop_icon
        # Re-queue the text and run in separate thread
        engine.say(extracted_text)
        threading.Thread(target=engine.runAndWait, daemon=True).start()
    else:
        # If icon is stop, stop playing audio
        pause_play_button.config(image=play_icon)
        pause_play_button.image = play_icon
        engine.stop()


# Function to generate navigation icons for audio playback
def generate_icons():
    convert_btn.pack_forget()
    control_frame.pack()
    pause_play_button.pack(side="left")
    speed_combo.pack(side="left", padx=12)


# Function to extract text from PDF
def get_text_from_pdf():
    global pdf_path
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    # cleaned_text = clean_text(text)
    clean_text = text.replace('\n', ' ').strip()
    return clean_text

# Function to convert PDF text to audio
def convert_audio():
    global extracted_text
    text_frame.pack(pady=10)
    generate_icons()
    text_area.pack(
        padx=5,
        pady=5,
        fill="both",
    )

    # Extract text from PDF and display it
    extracted_text = get_text_from_pdf()
    text_area.config(state="normal")        # temporarily enable to insert text
    text_area.delete("1.0", "end")          # clear any existing text
    text_area.insert("1.0", extracted_text) # insert extracted text
    text_area.config(state="disabled")      # disable editing again

# Title Label
title = tk.Label(
    window,
    text="Transform PDFs into Audio",
    fg="#5B4B8A",
    font=("Arial", 18, "bold"),
)
title.pack(pady=(20,10))

subtitle = tk.Label(
    window,
    text="upload, convert, and listen on the go",
    fg="#7B68B8",  # Medium purple
    font=("Arial", 11),
    bg=window_bg,
)
subtitle.pack(pady=(0,10))

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

# Control frame for backward, pause/play, and forward buttons
control_frame = tk.Frame(main_frame)


play_icon = find_img("./Assets/play.png", (35, 35))
stop_icon = find_img("./Assets/stop.png", (35, 35))
pause_play_button = tk.Button(
    control_frame,
    image=play_icon,
    bd=0,
    command=play_stop,
)
pause_play_button.image = play_icon  # Keep reference to the image


# Speed dropdown menu
speed_combo = ttk.Combobox(
    control_frame, values=["slow", "normal", "fast"], width=8,
)
speed_combo.set("normal")
speed_combo.config(state="readonly")
speed_combo.bind("<<ComboboxSelected>>", lambda e: speed_combo.selection_clear())


# Convert pdf text audio
convert_btn = tk.Button(window, text="Convert PDF to Audio", width=25, command=convert_audio)

# Text area to display pdf content
text_frame = tk.Frame(window)
text_area = tk.Text(
    text_frame,
    height=10,
    width=65,
    wrap="word",            # wrap text by word within the text area
    state="disabled",       # disable editing initially
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
pause_play_button.config(bg=window_bg, activebackground=window_bg)

window.mainloop()
