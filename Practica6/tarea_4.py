import tkinter as tk

window = tk.Tk()
window.title("Window Title")
window.geometry("120x80")

label = tk.Label(window, text="Red", fg="white", bg="red")
label.pack(pady=20, fill='x', side='right')

label = tk.Label(window, text="Blue", fg="white", bg="blue")
label.pack(pady=20, fill='x', side='left')

label = tk.Label(window, text="Green", fg="white", bg="green")
label.pack(pady=20, fill='x', side='right')


window.mainloop()
