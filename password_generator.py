from __future__ import annotations

import secrets
import string
import customtkinter as ctk
from tkinter import messagebox


MIN_LENGTH = 8
MAX_LENGTH = 32


def validate_length(value: str) -> int:
	
	value = value.strip()
	if not value:
		raise ValueError("Please enter a length.")

	length = int(value)
	if length < MIN_LENGTH or length > MAX_LENGTH:
		raise ValueError(
			f"Length must be between {MIN_LENGTH} and {MAX_LENGTH} characters."
		)

	return length


def generate_password(length: int) -> str:
	
	alphabet = string.ascii_letters + string.digits
	return "".join(secrets.choice(alphabet) for _ in range(length))


def on_generate(length_var: ctk.StringVar, output_var: ctk.StringVar) -> None:

	try:
		length = validate_length(length_var.get())
	except ValueError as exc:
		messagebox.showerror("Invalid Input", str(exc))
		return

	output_var.set(generate_password(length))


def main() -> None:

	ctk.set_appearance_mode("light")
	ctk.set_default_color_theme("blue")

	app = ctk.CTk()
	app.geometry("460x420")
	app.title("DecodeLabs Enterprise Password Generator")
	app.resizable(False, False)
	app.configure(fg_color="#F2EEE8")

	font_family = "trebuchet ms"

	length_var = ctk.StringVar(value=str(MIN_LENGTH))
	output_var = ctk.StringVar()

	title_label = ctk.CTkLabel(
		app,
		text="Enterprise Random Password Generator",
		font=(font_family, 20, "bold"),
		text_color="#2B2A28",
	)
	title_label.pack(pady=(20, 8))

	hint_label = ctk.CTkLabel(
		app,
		text=f"Allowed range: {MIN_LENGTH}-{MAX_LENGTH}",
		font=(font_family, 14),
		text_color="#5F5A52",
	)
	hint_label.pack(pady=(0, 16))

	length_row = ctk.CTkFrame(app, fg_color="transparent")
	length_row.pack(fill="x", padx=40, pady=6)

	length_label = ctk.CTkLabel(
		length_row,
		text="Password length",
		font=(font_family, 16),
		text_color="#2B2A28",
	)
	length_label.pack(side="left")

	length_entry = ctk.CTkEntry(
		length_row,
		textvariable=length_var,
		height=36,
		width=120,
		font=(font_family, 16),
		fg_color="#FFFDF9",
		text_color="#2B2A28",
		border_color="#BFAF9D",
	)
	length_entry.pack(side="right")
	length_entry.focus_set()

	generate_button = ctk.CTkButton(
		app,
		text="Generate Password",
		command=lambda: on_generate(length_var, output_var),
		height=42,
		font=(font_family, 16, "bold"),
		fg_color="#2F6B5F",
		hover_color="#27564C",
	)
	generate_button.pack(pady=18)

	output_label = ctk.CTkLabel(
		app,
		text="Generated password",
		font=(font_family, 16),
		text_color="#2B2A28",
	)
	output_label.pack(pady=(10, 6))

	output_entry = ctk.CTkEntry(
		app,
		textvariable=output_var,
		width=420,
		height=40,
		font=(font_family, 16),
		fg_color="#FFFDF9",
		text_color="#2B2A28",
		border_color="#BFAF9D",
		state="readonly",
	)
	output_entry.pack(pady=(0, 16))

	app.mainloop()


if __name__ == "__main__":
	main()
