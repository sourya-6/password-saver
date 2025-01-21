import tkinter as tk
from tkinter import messagebox
import json
import os

PASSKEY1 = "67890"
PASSKEY2 = "12345"
entered_passkeys = []
current_index = 0

# Load default credentials
def load_default_credentials():
    default_credentials = {
        "Email": {"username": "user@example.com", "password": "pass123"},
        "Bank": {"username": "user_bank", "password": "securepass"}
    }
    if not os.path.exists("credentials.json"):
        with open("credentials.json", "w") as f:
            json.dump(default_credentials, f, indent=4)

# Function to check passkeys and navigate accordingly
def check_passkey():
    entered_key = entry_passkey.get()
    entry_passkey.delete(0, tk.END)
    entered_passkeys.append(entered_key)
    
    if len(entered_passkeys) == 2:
        frame_passkey.pack_forget()
        if entered_passkeys[0] == PASSKEY1 and entered_passkeys[1] == PASSKEY2:
            frame_main.pack(fill=tk.BOTH, expand=True)
        else:
            frame_default.pack(fill=tk.BOTH, expand=True)
            show_saved_passwords()

# Function to toggle password visibility
def toggle_password(entry, button):
    if entry.cget('show') == '*':
        entry.config(show='')
        button.config(text='🙈')
    else:
        entry.config(show='*')
        button.config(text='👁')

# Function to display stored credentials one at a time
def show_saved_passwords():
    global current_index
    for widget in frame_saved_credentials.winfo_children():
        widget.destroy()

    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}

    keys = list(credentials.keys())
    if not keys:
        messagebox.showinfo("No Data", "No credentials saved yet.")
        return

    title = keys[current_index]
    creds = credentials[title]
    
    tk.Label(frame_saved_credentials, text=title, width=20).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame_saved_credentials, text=creds['username'], width=20).grid(row=0, column=1, padx=5, pady=5)
    
    password_entry = tk.Entry(frame_saved_credentials, width=20, show='*')
    password_entry.insert(0, creds['password'])
    password_entry.grid(row=0, column=2, padx=5, pady=5)
    
    toggle_button = tk.Button(frame_saved_credentials, text='👁', command=lambda: toggle_password(password_entry, toggle_button))
    toggle_button.grid(row=0, column=3, padx=5, pady=5)
    
    next_button = tk.Button(frame_saved_credentials, text='➡', command=show_next_password)
    next_button.grid(row=0, column=4, padx=5, pady=5)
    
    frame_saved_credentials.pack(fill=tk.BOTH, expand=True)

# Function to show next password
def show_next_password():
    global current_index
    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}
    
    if current_index < len(credentials) - 1:
        current_index += 1
    else:
        current_index = 0
    
    show_saved_passwords()

# Function to create virtual keyboard in the same tab
def show_virtual_keyboard(parent):
    keys = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
        'z', 'x', 'c', 'v', 'b', 'n', 'm'
    ]
    
    entry_focus = root.focus_get()
    
    def press_key(key):
        if entry_focus:
            entry_focus.insert(tk.END, key)
    
    keyboard_frame = tk.Frame(parent)
    keyboard_frame.pack()
    
    row, col = 0, 0
    for key in keys:
        tk.Button(keyboard_frame, text=key, command=lambda k=key: press_key(k)).grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 9:
            col = 0
            row += 1
    
    tk.Button(keyboard_frame, text='Space', command=lambda: press_key(' ')).grid(row=row+1, column=0, columnspan=5, padx=5, pady=5)
    tk.Button(keyboard_frame, text='Backspace', command=lambda: entry_focus.delete(len(entry_focus.get()) - 1, tk.END)).grid(row=row+1, column=5, columnspan=5, padx=5, pady=5)

root = tk.Tk()
root.title("Password Manager")
root.geometry("600x500")

frame_passkey = tk.Frame(root)
frame_passkey.pack()

label_passkey = tk.Label(frame_passkey, text="Enter Passkey:")
label_passkey.pack()
entry_passkey = tk.Entry(frame_passkey, width=10, show="*")
entry_passkey.pack()
button_virtual_keyboard = tk.Button(frame_passkey, text="⌨", command=lambda: show_virtual_keyboard(frame_passkey))
button_virtual_keyboard.pack()
button_submit_passkey = tk.Button(frame_passkey, text="Submit", command=check_passkey)
button_submit_passkey.pack()

frame_main = tk.Frame(root)
button_show_saved = tk.Button(frame_main, text="Show Saved Passwords", command=show_saved_passwords)
button_show_saved.pack()
frame_saved_credentials = tk.Frame(frame_main)

frame_default = tk.Frame(root)
button_show_default = tk.Button(frame_default, text="Show Default Passwords", command=show_saved_passwords)
button_show_default.pack()
frame_saved_credentials.pack()

load_default_credentials()
root.mainloop()
