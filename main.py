import tkinter as tk

window = tk.Tk()
window.title("PDF Audio")

label = tk.Label(window, text="Welcome to PDF Audio Application")
label.pack(pady=20)

convert_btn = tk.Button(window, text="Convert PDF to Audio")
convert_btn.pack(pady=10)

window.mainloop()