import tkinter as tk
from tkinter import messagebox
import json
import os

PASSKEY1 = "67890"
PASSKEY2 = "12345"
entered_passkeys = []
real_index = 0
fake_index = 0

# Initialize Tkinter window
root = tk.Tk()
root.title("Password Manager")
root.geometry("600x500")

# Load default credentials
def load_default_credentials():
    real_credentials = {
        "Email": {"username": "user@example.com", "password": "pass123"},
        "Bank": {"username": "user_bank", "password": "securepass"}
    }
    if not os.path.exists("credentials.json"):
        with open("credentials.json", "w") as f:
            json.dump(real_credentials, f, indent=4)

    fake_credentials = {
        "Social": {"username": "fake_user", "password": "fakepass"},
        "Game": {"username": "gamer123", "password": "gamepass"}
    }
    if not os.path.exists("fake_credentials.json"):
        with open("fake_credentials.json", "w") as f:
            json.dump(fake_credentials, f, indent=4)

# Function to check passkeys
def check_passkey():
    entered_key = entry_passkey.get()
    entry_passkey.delete(0, tk.END)
    entered_passkeys.append(entered_key)
    
    if len(entered_passkeys) == 2:
        frame_passkey.pack_forget()
        if entered_passkeys[0] == PASSKEY1 and entered_passkeys[1] == PASSKEY2:
            frame_real.pack(fill=tk.BOTH, expand=True)
        else:
            frame_fake.pack(fill=tk.BOTH, expand=True)
            show_fake_passwords()

# Function to toggle password visibility
def toggle_password(entry, button):
    if entry.cget('show') == '*':
        entry.config(show='')
        button.config(text='🙈')
    else:
        entry.config(show='*')
        button.config(text='👁')

# Function to exit application
def exit_application():
    root.destroy()

# === REAL CREDENTIALS ===
def show_real_passwords():
    global real_index
    real_index = 0
    display_real_credentials()

def display_real_credentials():
    global real_index
    for widget in frame_saved_real.winfo_children():
        widget.destroy()

    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}

    keys = list(credentials.keys())
    if not keys:
        messagebox.showinfo("No Data", "No real credentials saved yet.")
        return

    title = keys[real_index]
    creds = credentials[title]

    tk.Label(frame_saved_real, text=title, width=20).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame_saved_real, text=creds['username'], width=20).grid(row=0, column=1, padx=5, pady=5)

    password_entry = tk.Entry(frame_saved_real, width=20, show='*')
    password_entry.insert(0, creds['password'])
    password_entry.grid(row=0, column=2, padx=5, pady=5)

    toggle_button = tk.Button(frame_saved_real, text='👁', command=lambda: toggle_password(password_entry, toggle_button))
    toggle_button.grid(row=0, column=3, padx=5, pady=5)

    next_button = tk.Button(frame_saved_real, text='➡', command=next_real_password)
    next_button.grid(row=0, column=4, padx=5, pady=5)

    frame_saved_real.pack(fill=tk.BOTH, expand=True)

def next_real_password():
    global real_index
    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}

    if real_index < len(credentials) - 1:
        real_index += 1
    else:
        real_index = 0

    display_real_credentials()

# === FAKE CREDENTIALS ===
def show_fake_passwords():
    global fake_index
    fake_index = 0
    display_fake_credentials()

def display_fake_credentials():
    global fake_index
    for widget in frame_saved_fake.winfo_children():
        widget.destroy()

    if os.path.exists("fake_credentials.json"):
        with open("fake_credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}

    keys = list(credentials.keys())
    if not keys:
        messagebox.showinfo("No Data", "No fake credentials saved yet.")
        return

    title = keys[fake_index]
    creds = credentials[title]

    tk.Label(frame_saved_fake, text=title, width=20).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame_saved_fake, text=creds['username'], width=20).grid(row=0, column=1, padx=5, pady=5)

    password_entry = tk.Entry(frame_saved_fake, width=20, show='*')
    password_entry.insert(0, creds['password'])
    password_entry.grid(row=0, column=2, padx=5, pady=5)

    toggle_button = tk.Button(frame_saved_fake, text='👁', command=lambda: toggle_password(password_entry, toggle_button))
    toggle_button.grid(row=0, column=3, padx=5, pady=5)

    next_button = tk.Button(frame_saved_fake, text='➡', command=next_fake_password)
    next_button.grid(row=0, column=4, padx=5, pady=5)

    frame_saved_fake.pack(fill=tk.BOTH, expand=True)

def next_fake_password():
    global fake_index
    if os.path.exists("fake_credentials.json"):
        with open("fake_credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}

    if fake_index < len(credentials) - 1:
        fake_index += 1
    else:
        fake_index = 0

    display_fake_credentials()

# UI Design
frame_passkey = tk.Frame(root)
frame_passkey.pack()

label_passkey = tk.Label(frame_passkey, text="Enter Passkey:")
label_passkey.pack()
entry_passkey = tk.Entry(frame_passkey, width=10, show="*")
entry_passkey.pack()
button_submit_passkey = tk.Button(frame_passkey, text="Submit", command=check_passkey)
button_submit_passkey.pack()

frame_real = tk.Frame(root)
tk.Button(frame_real, text="Create New", command=show_real_passwords).pack()
tk.Button(frame_real, text="Show Saved Passwords", command=show_real_passwords).pack()
tk.Button(frame_real, text="Exit", command=exit_application).pack()
frame_saved_real = tk.Frame(frame_real)

frame_fake = tk.Frame(root)
tk.Button(frame_fake, text="Create New", command=show_fake_passwords).pack()
tk.Button(frame_fake, text="Show Saved Passwords", command=show_fake_passwords).pack()
tk.Button(frame_fake, text="Exit", command=exit_application).pack()
frame_saved_fake = tk.Frame(frame_fake)

# Load credentials
load_default_credentials()

# Start Tkinter event loop
root.mainloop()
