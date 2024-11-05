import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import numpy as np

# Function to perform SubBytes transformation
def sub_bytes(state):
    sbox = np.array([[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5],
                     [0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                     [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0],
                     [0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                     [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc],
                     [0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
                     [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a],
                     [0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
                     [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0],
                     [0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
                     [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b],
                     [0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
                     [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85],
                     [0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
                     [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5],
                     [0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
                     [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17],
                     [0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
                     [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88],
                     [0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
                     [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c],
                     [0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
                     [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9],
                     [0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
                     [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6],
                     [0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
                     [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e],
                     [0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
                     [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94],
                     [0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
                     [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68],
                     [0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]])
    
    for i in range(4):
        for j in range(4):
            state[i][j] = sbox[state[i][j] // 0x10][state[i][j] % 0x10]
    return state

# Function to perform ShiftRows transformation
def shift_rows(state):
    state[1] = np.roll(state[1], -1)  # Shift row 1 left by 1
    state[2] = np.roll(state[2], -2)  # Shift row 2 left by 2
    state[3] = np.roll(state[3], -3)  # Shift row 3 left by 3
    return state

# Function to perform MixColumns transformation
def mix_columns(state):
    for i in range(4):
        a = state[:, i]
        state[:, i] = [
            (2 * a[0] ^ 3 * a[1] ^ a[2] ^ a[3]) % 256,
            (a[0] ^ 2 * a[1] ^ 3 * a[2] ^ a[3]) % 256,
            (a[0] ^ a[1] ^ 2 * a[2] ^ 3 * a[3]) % 256,
            (3 * a[0] ^ a[1] ^ a[2] ^ 2 * a[3]) % 256,
        ]
    return state

# Function to add the round key
def add_round_key(state, round_key):
    return state ^ round_key

# Function to output the AES process
def output_aes_process(round_number, state, round_key):
    output_area.insert(tk.END, f"Round {round_number}:\n")
    output_area.insert(tk.END, f"State:\n{state}\n")
    output_area.insert(tk.END, f"Round Key:\n{round_key}\n\n")

# Function to encrypt the message
def encrypt_message():
    try:
        key_size = int(key_size_var.get())
        user_key = key_entry.get().encode()  # Convert input to bytes

        # Validate key length
        if len(user_key) != key_size // 8:
            messagebox.showerror("Error", f"Key must be {key_size // 8} bytes long.")
            return

        # Initialize AES cipher
        cipher = AES.new(user_key, AES.MODE_ECB)

        # Get input text and encode it
        plaintext = input_text.get("1.0", tk.END).strip()  # Get the plaintext
        padded_plaintext = pad(plaintext.encode(), 16)  # Pad plaintext to 16 bytes
        state = np.array([list(padded_plaintext[i:i + 4]) for i in range(0, 16)]).T  # Create initial state
        round_key = np.zeros((4, 4), dtype=np.uint8)  # Placeholder for round key

        # Output initial state
        output_aes_process(0, state, round_key)

        # Rounds
        for round_number in range(1, 11):  # 10 rounds for 128-bit key
            state = sub_bytes(state)
            state = shift_rows(state)
            if round_number < 10:  # MixColumns is not done in the final round
                state = mix_columns(state)
            state = add_round_key(state, round_key)  # Add round key for the demonstration
            output_aes_process(round_number, state, round_key)

        # Final round
        state = add_round_key(state, round_key)  # Add final round key
        output_area.insert(tk.END, f"Final State:\n{state}\n\n")

        ciphertext = cipher.encrypt(padded_plaintext)  # Encrypt the padded plaintext
        encrypted_text.delete("1.0", tk.END)
        encrypted_text.insert(tk.END, ciphertext.hex())  # Show encrypted text in hex
        messagebox.showinfo("Success", "Message encrypted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("AES Encryption/Decryption with Process Output")

# Create input text area
input_label = tk.Label(root, text="Input Message:")
input_label.pack()
input_text = tk.Text(root, height=5, width=50)
input_text.pack()

# Key size selection
key_size_label = tk.Label(root, text="Select Key Size (bits):")
key_size_label.pack()
key_size_var = tk.StringVar(value="128")  # Default value
key_size_dropdown = tk.OptionMenu(root, key_size_var, "128", "192", "256")
key_size_dropdown.pack()

# Secret key entry
key_entry_label = tk.Label(root, text="Enter Secret Key:")
key_entry_label.pack()
key_entry = tk.Entry(root, show="*")
key_entry.pack()

# Encrypt button
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_message)
encrypt_button.pack(pady=5)

# Encrypted text area
encrypted_label = tk.Label(root, text="Encrypted Message (Hex):")
encrypted_label.pack()
encrypted_text = tk.Text(root, height=5, width=50)
encrypted_text.pack()

# Output area for AES process
output_label = tk.Label(root, text="AES Process Output:")
output_label.pack()
output_area = tk.Text(root, height=10, width=50)
output_area.pack()

# Run the application
root.mainloop()
