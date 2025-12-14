import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import atexit

from networking import clientUDP

PRIMARY_BG = "#1f2430"
SECONDARY_BG = "#252c3b"
HIGHLIGHT_BG = "#30394d"
ACCENT = "#5eead4"
TEXT_COLOR = "#f8fafc"
SUBTLE_TEXT = "#94a3b8"

SERVER_PORT = 8000
USERNAME = input("Enter your username: ").strip() or "random_user"


def build_window() -> tk.Tk:
	window = tk.Tk()
	window.title("Discord.exe")
	window.geometry("960x600")
	window.minsize(720, 480)
	window.configure(bg=PRIMARY_BG)
	window.columnconfigure(0, weight=1)
	window.rowconfigure(0, weight=1)

	style = ttk.Style()
	available_themes = style.theme_names()
	theme = "clam" if "clam" in available_themes else available_themes[0]
	style.theme_use(theme)

	style.configure("Chat.TFrame", background=PRIMARY_BG)
	style.configure("Header.TFrame", background=SECONDARY_BG)
	style.configure("Sidebar.TFrame", background=HIGHLIGHT_BG)
	style.configure(
		"Accent.TButton",
		background=ACCENT,
		foreground="#0f172a",
		font=("Segoe UI Semibold", 11),
		padding=10,
		borderwidth=0,
	)
	style.map("Accent.TButton", background=[("active", "#3dd5ba")])

	style.configure("Outline.TButton", background=HIGHLIGHT_BG, foreground=SUBTLE_TEXT)
	style.configure(
		"Status.TLabel",
		background=SECONDARY_BG,
		foreground=SUBTLE_TEXT,
		font=("Segoe UI", 10),
	)
	style.configure(
		"Header.TLabel",
		background=SECONDARY_BG,
		foreground=TEXT_COLOR,
		font=("Segoe UI Semibold", 16),
	)

	return window


def build_layout(window: tk.Tk) -> dict:
	main = ttk.Frame(window, padding=20, style="Chat.TFrame")
	main.grid(row=0, column=0, sticky="nsew")
	main.columnconfigure(0, weight=3)
	main.columnconfigure(1, weight=1)
	main.rowconfigure(1, weight=1)

	# Header
	header = ttk.Frame(main, padding=(20, 12), style="Header.TFrame")
	header.grid(row=0, column=0, columnspan=2, sticky="ew")
	header.columnconfigure(0, weight=1)

	title = ttk.Label(header, text="Discord.exe", style="Header.TLabel")
	subtitle = ttk.Label(header, text="Secure chat • Online", style="Status.TLabel")
	title.grid(row=0, column=0, sticky="w")
	subtitle.grid(row=1, column=0, sticky="w")

	# Chat column
	chat_card = ttk.Frame(main, padding=0, style="Chat.TFrame")
	chat_card.grid(row=1, column=0, sticky="nsew", padx=(0, 18))
	chat_card.rowconfigure(0, weight=1)
	chat_card.columnconfigure(0, weight=1)

	chat_container = tk.Frame(chat_card, bg=SECONDARY_BG, bd=0, highlightthickness=0)
	chat_container.grid(row=0, column=0, sticky="nsew")
	chat_container.grid_rowconfigure(0, weight=1)
	chat_container.grid_columnconfigure(0, weight=1)

	chat_display = tk.Text(
		chat_container,
		bg=SECONDARY_BG,
		fg=TEXT_COLOR,
		relief="flat",
		wrap="word",
		font=("Segoe UI", 11),
		padx=20,
		pady=20,
		state="disabled",
	)
	chat_scroll = ttk.Scrollbar(chat_container, command=chat_display.yview)
	chat_display.configure(yscrollcommand=chat_scroll.set)
	chat_display.grid(row=0, column=0, sticky="nsew")
	chat_scroll.grid(row=0, column=1, sticky="ns")
	chat_display.tag_configure("meta", foreground=SUBTLE_TEXT, font=("Segoe UI", 9, "italic"))

	# Sidebar for people online
	sidebar = ttk.Frame(main, padding=18, style="Sidebar.TFrame")
	sidebar.grid(row=1, column=1, sticky="nsew")
	sidebar.columnconfigure(0, weight=1)

	tk.Label(
		sidebar,
		text="Now chatting",
		fg=TEXT_COLOR,
		bg=HIGHLIGHT_BG,
		font=("Segoe UI Semibold", 12),
	).grid(row=0, column=0, sticky="w")

	user_container = tk.Frame(sidebar, bg=HIGHLIGHT_BG)
	user_container.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
	sidebar.rowconfigure(1, weight=1)

	# Composer row
	composer = tk.Frame(main, bg=PRIMARY_BG)
	composer.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(18, 0))
	composer.columnconfigure(1, weight=1)

	message_var = tk.StringVar()

	attach_btn = ttk.Button(
		composer,
		text="＋",
		width=3,
		style="Outline.TButton",
		command=lambda: insert_status_message(chat_display, "Attachment picker coming soon"),
	)
	attach_btn.grid(row=0, column=0, padx=(0, 10))

	entry = tk.Entry(
		composer,
		textvariable=message_var,
		font=("Segoe UI", 11),
		relief="flat",
		bg=SECONDARY_BG,
		fg=TEXT_COLOR,
		insertbackground=TEXT_COLOR,
	)
	entry.grid(row=0, column=1, sticky="ew")

	send_btn = ttk.Button(
		composer,
		text="Send",
		style="Accent.TButton",
		command=lambda: send_message(message_var, chat_display),
	)
	send_btn.grid(row=0, column=2, padx=(10, 0))

	return {
		"chat_display": chat_display,
		"message_var": message_var,
		"entry": entry,
		"window": window,
		"user_container": user_container,
		"send_btn": send_btn,
	}


def set_users(user_container: tk.Frame, users: list[str]) -> None:
	for widget in user_container.winfo_children():
		widget.destroy()

	if not users:
		tk.Label(
			user_container,
			text="Nobody is online yet",
			fg=SUBTLE_TEXT,
			bg=HIGHLIGHT_BG,
			font=("Segoe UI", 10),
		).pack(anchor="w")
		return

	for username in users:
		tk.Label(
			user_container,
			text=username,
			anchor="w",
			justify="left",
			bg=HIGHLIGHT_BG,
			fg=ACCENT if username == f"@{USERNAME}" else TEXT_COLOR,
			font=("Segoe UI", 11),
			padx=8,
			pady=4,
		).pack(fill="x", pady=2)


def append_message(
	chat_display: tk.Text,
	sender: str,
	content: str,
	*,
	timestamp: str | None = None,
) -> None:
	ts = timestamp or datetime.now().strftime("%H:%M")
	chat_display.configure(state="normal")
	chat_display.insert("end", f"{sender} • {ts}\n", "meta")
	chat_display.insert("end", f"{content}\n\n")
	chat_display.configure(state="disabled")
	chat_display.see("end")


def set_messages(chat_display: tk.Text, messages: list[dict[str, str]]) -> None:
	chat_display.configure(state="normal")
	chat_display.delete("1.0", "end")
	for message in messages:
		append_message(
			chat_display,
			message.get("sender", "Unknown"),
			message.get("content", ""),
			timestamp=message.get("timestamp"),
		)
	chat_display.configure(state="disabled")


def start_listener(ui_state: dict) -> None:
	def listen_loop():
		client = ui_state["client"]
		while True:
			incoming = client.listen()
			data = incoming["data"]
			ui_state["window"].after(0, parse_incoming_message, data, ui_state)

	threading.Thread(target=listen_loop, daemon=True).start()


def insert_status_message(chat_display: tk.Text, message: str) -> None:
	chat_display.configure(state="normal")
	chat_display.insert("end", f"⚙ {message}\n", "meta")
	chat_display.insert("end", "\n")
	chat_display.configure(state="disabled")
	chat_display.see("end")


def send_message(
	message_var: tk.StringVar,
	chat_display: tk.Text,
	*,
	client: clientUDP.ClientUDP | None = None,
	server_ip: str | None = None,
	server_port: int | None = None,
	username: str = USERNAME,
) -> None:
	message = message_var.get().strip()
	if not message:
		return

	append_message(chat_display, "You", message)

	if client and server_ip and server_port:
		payload = f"message<sp>{username}<sp>{message}"
		client.send_to(payload, server_ip, server_port)

	message_var.set("")


def parse_incoming_message(data: str, ui_state: dict) -> None:
	parts = data.split("<sp>")
	command = parts[0]
	widgets = ui_state["widgets"]

	if command == "users":
		users = [f"@{username}" for username in parts[1:]]
		ui_state["users"] = users
		set_users(widgets["user_container"], users)

	elif command == "message":
		sender = parts[1]
		content = parts[2] if len(parts) > 2 else ""
		message_record = {
			"sender": sender,
			"content": content,
			"timestamp": datetime.now().strftime("%H:%M"),
		}
		ui_state["messages"].append(message_record)
		set_messages(widgets["chat_display"], ui_state["messages"])

def main():
	client = clientUDP.ClientUDP()
	server_ip = client.LOCAL_IP  # assuming local testing
	client.send_to(
		data=f"connect<sp>{USERNAME}",
		target_ip=server_ip,
		target_port=SERVER_PORT,
	)
	atexit.register(lambda: client.send_to(
		data=f"disconnect<sp>{USERNAME}",
		target_ip=server_ip,
		target_port=SERVER_PORT,
	))
	window = build_window()
	widgets = build_layout(window)

	ui_state = {
		"window": window,
		"widgets": widgets,
		"client": client,
		"server_ip": server_ip,
		"server_port": SERVER_PORT,
		"username": USERNAME,
		"messages": [],
		"users": [],
	}

	set_users(widgets["user_container"], [])
	insert_status_message(widgets["chat_display"], "Welcome to Discord.exe")

	send_command = lambda: send_message(
		widgets["message_var"],
		widgets["chat_display"],
		client=client,
		server_ip=server_ip,
		server_port=SERVER_PORT,
		username=USERNAME,
	)
	widgets["send_btn"].configure(command=send_command)
	window.bind("<Return>", lambda event: send_command())

	start_listener(ui_state)

	widgets["entry"].focus_set()
	window.mainloop()


if __name__ == "__main__":
	main()