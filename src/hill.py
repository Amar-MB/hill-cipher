import tkinter as tk
from tkinter import messagebox


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KEY = ((3, 3), (2, 5))
MODULUS = len(ALPHABET)


def encrypt_block(block):
	"""Encrypt two uppercase letters with the example Hill cipher key."""
	values = [ALPHABET.index(letter) for letter in block]
	encrypted = [
		sum(KEY[row][column] * values[column] for column in range(2)) % MODULUS
		for row in range(2)
	]
	return values, encrypted


class HillCipherVisualizer(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Hill Cipher Visualizer")
		self.geometry("760x520")
		self.minsize(620, 460)
		self.configure(bg="#f3f5f4")

		self.blocks = []
		self.block_index = 0
		self.plaintext = ""
		self.ciphertext = ""

		header = tk.Frame(self, bg="#f3f5f4", padx=24, pady=18)
		header.pack(fill="x")
		tk.Label(
			header,
			text="HILL CIPHER",
			font=("Segoe UI", 19, "bold"),
			fg="#183d36",
			bg="#f3f5f4",
		).pack(anchor="w")
		tk.Label(
			header,
			text="2 x 2 matrix encryption modulo 26",
			font=("Segoe UI", 10),
			fg="#52645e",
			bg="#f3f5f4",
		).pack(anchor="w", pady=(2, 12))

		controls = tk.Frame(header, bg="#f3f5f4")
		controls.pack(fill="x")
		tk.Label(controls, text="Plaintext", font=("Segoe UI", 10), bg="#f3f5f4").pack(side="left")
		self.input_var = tk.StringVar(value="HELP")
		self.input = tk.Entry(controls, textvariable=self.input_var, font=("Consolas", 12), width=24)
		self.input.pack(side="left", padx=(9, 10))
		self.input.bind("<Return>", lambda _event: self.encrypt())
		tk.Button(
			controls,
			text="Encrypt",
			command=self.encrypt,
			font=("Segoe UI", 10, "bold"),
			bg="#176b57",
			fg="white",
			activebackground="#125645",
			activeforeground="white",
			relief="flat",
			padx=14,
			pady=6,
		).pack(side="left")

		self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
		self.canvas.pack(fill="both", expand=True, padx=24)
		self.canvas.bind("<Configure>", lambda _event: self.draw())

		footer = tk.Frame(self, bg="#f3f5f4", padx=24, pady=14)
		footer.pack(fill="x")
		self.result_label = tk.Label(
			footer, text="Ciphertext: -", font=("Consolas", 12, "bold"), fg="#183d36", bg="#f3f5f4"
		)
		self.result_label.pack(side="left")
		self.previous_button = tk.Button(footer, text="Previous", command=self.previous, state="disabled")
		self.previous_button.pack(side="right", padx=(8, 0))
		self.next_button = tk.Button(footer, text="Next", command=self.next, state="disabled")
		self.next_button.pack(side="right")

		self.encrypt()

	def encrypt(self):
		letters = "".join(letter for letter in self.input_var.get().upper() if letter in ALPHABET)
		if not letters:
			messagebox.showerror("Invalid plaintext", "Enter at least one letter from A to Z.")
			return

		if len(letters) % 2:
			letters += "X"

		self.plaintext = letters
		self.blocks = [letters[index:index + 2] for index in range(0, len(letters), 2)]
		self.block_index = 0
		encrypted_blocks = []
		for block in self.blocks:
			_values, encrypted = encrypt_block(block)
			encrypted_blocks.append("".join(ALPHABET[value] for value in encrypted))
		self.ciphertext = "".join(encrypted_blocks)
		self.result_label.config(text=f"Ciphertext: {self.ciphertext}")
		self.update_navigation()
		self.draw()

	def previous(self):
		self.block_index = max(0, self.block_index - 1)
		self.update_navigation()
		self.draw()

	def next(self):
		self.block_index = min(len(self.blocks) - 1, self.block_index + 1)
		self.update_navigation()
		self.draw()

	def update_navigation(self):
		self.previous_button.config(state="normal" if self.block_index > 0 else "disabled")
		self.next_button.config(state="normal" if self.block_index < len(self.blocks) - 1 else "disabled")

	def draw(self):
		if not hasattr(self, "canvas"):
			return
		self.canvas.delete("all")
		width = max(self.canvas.winfo_width(), 1)
		center = width / 2
		self.canvas.create_text(
			center, 32, text="C = K 3 P (mod 26)", font=("Consolas", 17, "bold"), fill="#183d36"
		)
		self.canvas.create_text(
			center, 62, text="A = 0, B = 1, ... Z = 25", font=("Segoe UI", 10), fill="#52645e"
		)

		if not self.blocks:
			return

		block = self.blocks[self.block_index]
		plain_values, cipher_values = encrypt_block(block)
		cipher_block = "".join(ALPHABET[value] for value in cipher_values)
		self.canvas.create_text(
			center, 105, text=f"Block {self.block_index + 1} of {len(self.blocks)}",
			font=("Segoe UI", 11, "bold"), fill="#176b57"
		)

		positions = (center - 220, center - 55, center + 95, center + 240)
		self.canvas.create_text(positions[0], 145, text="KEY MATRIX", font=("Segoe UI", 9, "bold"), fill="#52645e")
		self.canvas.create_text(positions[0], 192, text="[ 3  3 ]\n[ 2  5 ]", font=("Consolas", 18), fill="#183d36", justify="center")
		self.canvas.create_text(positions[1], 145, text="PLAINTEXT", font=("Segoe UI", 9, "bold"), fill="#52645e")
		self.canvas.create_text(positions[1], 192, text=f"[{block[0]}] = [{plain_values[0]}]\n[{block[1]}]   [{plain_values[1]}]", font=("Consolas", 15), fill="#183d36", justify="center")
		self.canvas.create_text(positions[2], 192, text="×", font=("Segoe UI", 22), fill="#8b9892")
		self.canvas.create_text(positions[3], 145, text="CIPHERTEXT", font=("Segoe UI", 9, "bold"), fill="#52645e")
		self.canvas.create_text(positions[3], 192, text=f"[{cipher_block[0]}] = [{cipher_values[0]}]\n[{cipher_block[1]}]   [{cipher_values[1]}]", font=("Consolas", 15, "bold"), fill="#176b57", justify="center")

		self.canvas.create_line(32, 246, width - 32, 246, fill="#e1e8e4")
		row_one = (KEY[0][0] * plain_values[0] + KEY[0][1] * plain_values[1])
		row_two = (KEY[1][0] * plain_values[0] + KEY[1][1] * plain_values[1])
		self.canvas.create_text(42, 278, anchor="w", text="ROW-BY-ROW MODULAR ARITHMETIC", font=("Segoe UI", 9, "bold"), fill="#52645e")
		self.canvas.create_text(
			42, 323,
			anchor="w",
			text=f"C1 = (3 x {plain_values[0]} + 3 x {plain_values[1]}) mod 26 = {row_one} mod 26 = {cipher_values[0]} -> {cipher_block[0]}",
			font=("Consolas", 11),
			fill="#183d36",
		)
		self.canvas.create_text(
			42, 363,
			anchor="w",
			text=f"C2 = (2 x {plain_values[0]} + 5 x {plain_values[1]}) mod 26 = {row_two} mod 26 = {cipher_values[1]} -> {cipher_block[1]}",
			font=("Consolas", 11),
			fill="#183d36",
		)
		self.canvas.create_text(
			center, 414,
			text=f"{block[0]}{block[1]}  ->  [{plain_values[0]}, {plain_values[1]}]  ->  [{cipher_values[0]}, {cipher_values[1]}]  ->  {cipher_block}",
			font=("Consolas", 12, "bold"),
			fill="#176b57",
		)


if __name__ == "__main__":
	HillCipherVisualizer().mainloop()
