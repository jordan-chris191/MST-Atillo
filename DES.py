import tkinter as tk
from tkinter import messagebox, ttk
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

def update_key_length():
    """Update the label with the number of bytes in the entered secret key."""
    user_key = key_entry.get().encode()  # Convert input to bytes
    key_length_label.config(text=f"Key Length: {len(user_key)} bytes")  # Update label

def encrypt_message():
    try:
        user_key = key_entry.get().encode()  # Convert input to bytes

        # Validate key length
        if len(user_key) != 8:
            messagebox.showerror("Error", "Key must be 8 bytes long for DES.")
            return

        # Get input text and encode it
        plaintext = encrypt_input_text.get("1.0", tk.END).strip()  # Get the plaintext

        # Choose padding method
        padding_method = padding_var.get()
        if padding_method == "PKCS7":
            padded_plaintext = pad(plaintext.encode(), 8)  # Pad plaintext to 8 bytes using PKCS7
        else:  # Zero Padding
            padded_plaintext = plaintext.encode() + b'\x00' * (8 - len(plaintext) % 8)  # Zero pad

        # Initialize DES cipher
        cipher = DES.new(user_key, DES.MODE_ECB)
        
        # Encrypt the padded plaintext
        ciphertext = cipher.encrypt(padded_plaintext)

        # Get selected output format
        output_format = output_format_var.get()
        if output_format == "hex":
            output = ciphertext.hex()  # Show encrypted text in hex
        else:  # Base64
            output = base64.b64encode(ciphertext).decode()  # Show encrypted text in Base64
        
        # Output encrypted text
        encrypted_output_text.delete("1.0", tk.END)
        encrypted_output_text.insert(tk.END, output)  # Show encrypted text
        messagebox.showinfo("Success", "Message encrypted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_message():
    try:
        user_key = key_entry.get().encode()  # Convert input to bytes

        # Validate key length
        if len(user_key) != 8:
            messagebox.showerror("Error", "Key must be 8 bytes long for DES.")
            return

        # Get the hex or Base64 input for decryption
        hex_input = decrypt_input_text.get("1.0", tk.END).strip()  # Get the encrypted message
        output_format = output_format_var.get()

        if output_format == "hex":
            ciphertext = bytes.fromhex(hex_input)  # Convert hex to bytes
        else:  # Base64
            ciphertext = base64.b64decode(hex_input)  # Decode Base64 to bytes

        # Initialize DES cipher
        cipher = DES.new(user_key, DES.MODE_ECB)
        
        # Decrypt the ciphertext
        padded_plaintext = cipher.decrypt(ciphertext)

        # Choose padding method for unpadding
        padding_method = padding_var.get()
        if padding_method == "PKCS7":
            plaintext = unpad(padded_plaintext, 8).decode()  # Unpad to get original plaintext using PKCS7
        else:  # Zero Padding
            plaintext = padded_plaintext.rstrip(b'\x00').decode()  # Remove zero padding

        # Output decrypted text
        decrypted_output_text.delete("1.0", tk.END)
        decrypted_output_text.insert(tk.END, plaintext)  # Show decrypted text
        messagebox.showinfo("Success", "Message decrypted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("DES Encryption/Decryption")

# Set a modern style
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 10), padding=5)
style.configure("TEntry", font=("Helvetica", 10), padding=5)
style.configure("TText", font=("Helvetica", 10), padding=5)

# Create a frame for the encryption and decryption layout
main_frame = ttk.Frame(root)
main_frame.pack(pady=10)

# Create left frame for encryption
encrypt_frame = ttk.Frame(main_frame)
encrypt_frame.pack(side=tk.LEFT, padx=10)

# Input text area for encryption
encrypt_label = ttk.Label(encrypt_frame, text="Input Message for Encryption:")
encrypt_label.pack(pady=(10, 0))
encrypt_input_frame = ttk.Frame(encrypt_frame)
encrypt_input_frame.pack()

encrypt_input_text = tk.Text(encrypt_input_frame, height=6, width=50)
encrypt_input_text.pack(side=tk.LEFT)

encrypt_input_scrollbar = tk.Scrollbar(encrypt_input_frame, command=encrypt_input_text.yview)
encrypt_input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
encrypt_input_text.config(yscrollcommand=encrypt_input_scrollbar.set)

# Secret key entry for encryption
key_entry_label = ttk.Label(encrypt_frame, text="Enter Secret Key (8 bytes):")
key_entry_label.pack(pady=(10, 0))
key_entry = ttk.Entry(encrypt_frame)  # Removed show="*"
key_entry.pack(pady=5)
key_entry.bind("<KeyRelease>", lambda event: update_key_length())  # Update key length on key release

# Key length display for encryption
key_length_label = ttk.Label(encrypt_frame, text="Key Length: 0 bytes")
key_length_label.pack(pady=(5, 0))

# Output format selection for encryption
output_format_label = ttk.Label(encrypt_frame, text="Select Output Format:")
output_format_label.pack(pady=(10, 0))
output_format_var = tk.StringVar(value="hex")  # Default value
hex_radio = ttk.Radiobutton(encrypt_frame, text="Hex", variable=output_format_var, value="hex")
base64_radio = ttk.Radiobutton(encrypt_frame, text="Base64", variable=output_format_var, value="base64")
hex_radio.pack(pady=2)
base64_radio.pack(pady=2)

# Padding selection for encryption
padding_label = ttk.Label(encrypt_frame, text="Select Padding Method:")
padding_label.pack(pady=(10, 0))
padding_var = tk.StringVar(value="PKCS7")  # Default value
padding_dropdown = ttk.OptionMenu(encrypt_frame, padding_var, "PKCS7", "PKCS7", "Zero Padding")
padding_dropdown.pack(pady=5)

# Encrypt button
encrypt_button = ttk.Button(encrypt_frame, text="Encrypt", command=encrypt_message)
encrypt_button.pack(pady=(10, 5))

# Encrypted text area for output
encrypted_label = ttk.Label(encrypt_frame, text="Encrypted Message (Hex/Base64):")
encrypted_label.pack(pady=(10, 0))
encrypted_output_frame = ttk.Frame(encrypt_frame)
encrypted_output_frame.pack()

encrypted_output_text = tk.Text(encrypted_output_frame, height=6, width=50)
encrypted_output_text.pack(side=tk.LEFT)

encrypted_output_scrollbar = tk.Scrollbar(encrypted_output_frame, command=encrypted_output_text.yview)
encrypted_output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
encrypted_output_text.config(yscrollcommand=encrypted_output_scrollbar.set)

# Create right frame for decryption
decrypt_frame = ttk.Frame(main_frame)
decrypt_frame.pack(side=tk.RIGHT, padx=10)

# Input text area for decryption
decrypt_label = ttk.Label(decrypt_frame, text="Input Encrypted Message:")
decrypt_label.pack(pady=(10, 0))
decrypt_input_frame = ttk.Frame(decrypt_frame)
decrypt_input_frame.pack()

decrypt_input_text = tk.Text(decrypt_input_frame, height=6, width=50)
decrypt_input_text.pack(side=tk.LEFT)

decrypt_input_scrollbar = tk.Scrollbar(decrypt_input_frame, command=decrypt_input_text.yview)
decrypt_input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
decrypt_input_text.config(yscrollcommand=decrypt_input_scrollbar.set)

# Secret key entry for decryption (same as encryption)
decrypt_key_entry_label = ttk.Label(decrypt_frame, text="Enter Secret Key (8 bytes):")
decrypt_key_entry_label.pack(pady=(10, 0))
decrypt_key_entry = ttk.Entry(decrypt_frame)  # Removed show="*"
decrypt_key_entry.pack(pady=5)

# Key length display for decryption
decrypt_key_length_label = ttk.Label(decrypt_frame, text="Key Length: 0 bytes")
decrypt_key_length_label.pack(pady=(5, 0))

# Output format selection for decryption (same as encryption)
decrypt_output_format_label = ttk.Label(decrypt_frame, text="Select Output Format:")
decrypt_output_format_label.pack(pady=(10, 0))
decrypt_output_format_var = tk.StringVar(value="hex")  # Default value
decrypt_hex_radio = ttk.Radiobutton(decrypt_frame, text="Hex", variable=decrypt_output_format_var, value="hex")
decrypt_base64_radio = ttk.Radiobutton(decrypt_frame, text="Base64", variable=decrypt_output_format_var, value="base64")
decrypt_hex_radio.pack(pady=2)
decrypt_base64_radio.pack(pady=2)

# Padding selection for decryption (same as encryption)
decrypt_padding_label = ttk.Label(decrypt_frame, text="Select Padding Method:")
decrypt_padding_label.pack(pady=(10, 0))
decrypt_padding_var = tk.StringVar(value="PKCS7")  # Default value
decrypt_padding_dropdown = ttk.OptionMenu(decrypt_frame, decrypt_padding_var, "PKCS7", "PKCS7", "Zero Padding")
decrypt_padding_dropdown.pack(pady=5)

# Decrypt button
decrypt_button = ttk.Button(decrypt_frame, text="Decrypt", command=decrypt_message)
decrypt_button.pack(pady=(10, 5))

# Decrypted text area for output
decrypted_label = ttk.Label(decrypt_frame, text="Decrypted Message:")
decrypted_label.pack(pady=(10, 0))
decrypted_output_frame = ttk.Frame(decrypt_frame)
decrypted_output_frame.pack()

decrypted_output_text = tk.Text(decrypted_output_frame, height=6, width=50)
decrypted_output_text.pack(side=tk.LEFT)

decrypted_output_scrollbar = tk.Scrollbar(decrypted_output_frame, command=decrypted_output_text.yview)
decrypted_output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
decrypted_output_text.config(yscrollcommand=decrypted_output_scrollbar.set)

# Start the Tkinter main loop
root.mainloop()