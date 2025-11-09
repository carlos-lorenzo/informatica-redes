import tkinter as tk

window = tk.Tk()
window.title("Window with Grid")
window.geometry("400x300")

description_label = tk.Label(
    window, text="Here we'll copy the text from below")
description_label.grid(row=0, column=0, columnspan=2, pady=10)

entry = tk.Entry(window)
entry.grid(row=1, column=0, padx=10, pady=10)

copy_button = tk.Button(
    window, text="Copy", command=lambda: description_label.config(text=entry.get()))
copy_button.grid(row=1, column=1, padx=10, pady=10)

window.mainloop()
