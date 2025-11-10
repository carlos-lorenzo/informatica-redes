import tkinter as tk

window = tk.Tk()
window.title("Message Box Example")
window.geometry("400x300")


def update_message():
    text = text_enter.get()
    text_enter.delete(0, tk.END)
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, text)
    text_area.config(state=tk.DISABLED)


# Text area
text_area = tk.Text(window, height=10, width=40)
text_area.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Footer options

footer = tk.Frame(window)
footer.grid(row=4, column=0, columnspan=4, pady=10)
text_enter = tk.Entry(footer, width=30)
text_enter.grid(row=4, column=0, columnspan=3)

send_text = tk.Button(
    footer, text="Copy", command=lambda: update_message())
send_text.grid(row=4, column=4, pady=10)

window.mainloop()
