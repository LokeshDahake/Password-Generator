import tkinter as tk
import random
import string
import re
from tkinter import messagebox

# List of common words to avoid in passwords (simple example, you can expand this list)
COMMON_WORDS = ['password', '1234', 'qwerty', 'letmein', 'admin', 'welcome', 'iloveyou', 'monkey']

def check_password_strength(password):
    # Check length
    if len(password) < 12:
        return "Weak", "red"
    
    # Check character variety
    if not (any(c.islower() for c in password) and any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and any(c in string.punctuation for c in password)):
        return "Medium", "orange"
    
    # Avoid common patterns
    if re.search(r'(.)\1{2,}', password):  # Check for repeating characters
        return "Weak", "red"
    
    # Avoid dictionary words
    if any(word in password.lower() for word in COMMON_WORDS):
        return "Weak", "red"
    
    return "Strong", "green"

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")
        self.master.geometry("450x500")

        # Bind the Enter key to the generate_password function
        self.master.bind('<Return>', self.generate_password)

        # Label for password length
        self.label = tk.Label(master, text="Enter total password length:")
        self.label.pack(pady=10)

        # Entry for total password length
        self.length_entry = tk.Entry(master)
        self.length_entry.pack(pady=5)

        # Label for letters, digits, and symbols
        self.letters_label = tk.Label(master, text="How many letters to include?")
        self.letters_label.pack(pady=5)

        self.letters_entry = tk.Entry(master)
        self.letters_entry.pack(pady=5)

        self.digits_label = tk.Label(master, text="How many digits to include?")
        self.digits_label.pack(pady=5)

        self.digits_entry = tk.Entry(master)
        self.digits_entry.pack(pady=5)

        self.symbols_label = tk.Label(master, text="How many symbols to include?")
        self.symbols_label.pack(pady=5)

        self.symbols_entry = tk.Entry(master)
        self.symbols_entry.pack(pady=5)

        # Button to generate password
        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=10)

        # Display generated password
        self.password_display = tk.Entry(master, width=30, font=('Arial', 14))
        self.password_display.pack(pady=20)

        # Password strength label
        self.strength_label = tk.Label(master, text="Password Strength: Not Generated", fg="gray")
        self.strength_label.pack(pady=5)

        # Copy password button
        self.copy_button = tk.Button(master, text="Copy to Clipboard", command=self.copy_password)
        self.copy_button.pack(pady=10)

        # Clear button
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_fields)
        self.clear_button.pack(pady=5)

    def generate_password(self, event=None):
        try:
            # Get values from the user input
            total_length = int(self.length_entry.get())
            letters_count = self.get_input(self.letters_entry.get(), max(total_length // 3, 5))  # Ensure at least 5 letters
            digits_count = self.get_input(self.digits_entry.get(), total_length // 3)
            symbols_count = self.get_input(self.symbols_entry.get(), total_length // 3)

            # Ensure that at least 5 letters are included
            if letters_count < 5:
                letters_count = 5

            # Ensure total length is valid
            if total_length <= 0:
                raise ValueError("Password length must be greater than zero.")
            if letters_count + digits_count + symbols_count > total_length:
                raise ValueError("The sum of letters, digits, and symbols cannot exceed the total length.")

            # Generate password based on user inputs
            letters = string.ascii_letters
            digits = string.digits
            symbols = string.punctuation

            password = []

            # Add letters, digits, and symbols based on the user's selection
            password.extend(random.choices(letters, k=letters_count))
            password.extend(random.choices(digits, k=digits_count))
            password.extend(random.choices(symbols, k=symbols_count))

            # Shuffle the password to ensure randomness
            random.shuffle(password)

            password = ''.join(password)

            # Display the generated password
            self.password_display.delete(0, tk.END)
            self.password_display.insert(0, password)

            # Check and display password strength
            strength, color = check_password_strength(password)
            self.strength_label.config(text=f"Password Strength: {strength}", fg=color)

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def copy_password(self):
        password = self.password_display.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    def clear_fields(self):
        # Clear all input fields and reset the strength label
        self.length_entry.delete(0, tk.END)
        self.letters_entry.delete(0, tk.END)
        self.digits_entry.delete(0, tk.END)
        self.symbols_entry.delete(0, tk.END)
        self.password_display.delete(0, tk.END)
        self.strength_label.config(text="Password Strength: Not Generated", fg="gray")

    def get_input(self, input_value, default):
        try:
            return int(input_value) if input_value else default
        except ValueError:
            return default

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()