import tkinter as tk

window = tk.Tk()
window.title("Window Title")
window.geometry("400x300")

label = tk.Label(window, text="¡Hola, Tkinter!")
label.pack(pady=20)


window.mainloop()
