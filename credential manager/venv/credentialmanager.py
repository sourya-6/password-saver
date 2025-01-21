import tkinter as tk
from tkinter import messagebox
import json
import os

PASSKEY1 = "67890"
PASSKEY2 = "12345"
entered_passkeys = []

# Function to check passkeys and navigate accordingly
def check_passkey():
    entered_key = entry_passkey.get()
    entry_passkey.delete(0, tk.END)
    entered_passkeys.append(entered_key)
    
    if len(entered_passkeys) == 2:
        if entered_passkeys[0] == PASSKEY1 and entered_passkeys[1] == PASSKEY2:
            frame_passkey.pack_forget()
            frame_main.pack(fill=tk.BOTH, expand=True)
        else:
            frame_passkey.pack_forget()
            frame_default.pack(fill=tk.BOTH, expand=True)
    
# Function to save new credentials
def save_credentials():
    title = entry_title.get()
    username = entry_username.get()
    password = entry_password.get()

    if not title or not username or not password:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}

    credentials[title] = {"username": username, "password": password}

    with open("credentials.json", "w") as f:
        json.dump(credentials, f, indent=4)

    entry_title.delete(0, tk.END)
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    messagebox.showinfo("Success", "Credentials saved successfully!")

# Function to toggle password visibility
def toggle_password():
    if entry_password.cget('show') == '*':
        entry_password.config(show='')
    else:
        entry_password.config(show='*')

# Function to display stored credentials
def show_saved_passwords():
    for widget in frame_saved_credentials.winfo_children():
        widget.destroy()

    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}

    if not credentials:
        messagebox.showinfo("No Data", "No credentials saved yet.")
        return

    for row, (title, creds) in enumerate(credentials.items(), start=1):
        tk.Label(frame_saved_credentials, text=title, width=20).grid(row=row, column=0, padx=5, pady=5)
        tk.Label(frame_saved_credentials, text=creds['username'], width=20).grid(row=row, column=1, padx=5, pady=5)
        tk.Label(frame_saved_credentials, text=creds['password'], width=20).grid(row=row, column=2, padx=5, pady=5)
    
    frame_saved_credentials.pack(fill=tk.BOTH, expand=True)

# Function to create new credentials
def create_new_credentials():
    frame_saved_credentials.pack_forget()
    frame_create.pack(fill=tk.BOTH, expand=True)

def exit_application():
    root.quit()

root = tk.Tk()
root.title("Password Manager")
root.geometry("600x400")

frame_passkey = tk.Frame(root)
frame_passkey.pack()

label_passkey = tk.Label(frame_passkey, text="Enter Passkey:")
label_passkey.pack()
entry_passkey = tk.Entry(frame_passkey, width=10, show="*")
entry_passkey.pack()
button_submit_passkey = tk.Button(frame_passkey, text="Submit", command=check_passkey)
button_submit_passkey.pack()

frame_main = tk.Frame(root)

button_create_new = tk.Button(frame_main, text="Create New", command=create_new_credentials)
button_create_new.pack(side=tk.LEFT, padx=20, pady=20)

button_show_saved = tk.Button(frame_main, text="Show Saved Passwords", command=show_saved_passwords)
button_show_saved.pack(side=tk.LEFT, padx=20, pady=20)

button_exit = tk.Button(frame_main, text="Exit", command=exit_application)
button_exit.pack(side=tk.BOTTOM, pady=20)

frame_create = tk.Frame(frame_main)

label_title = tk.Label(frame_create, text="Title:")
label_title.pack()
entry_title = tk.Entry(frame_create, width=30)
entry_title.pack()

label_username = tk.Label(frame_create, text="Username:")
label_username.pack()
entry_username = tk.Entry(frame_create, width=30)
entry_username.pack()

label_password = tk.Label(frame_create, text="Password:")
label_password.pack()
entry_password = tk.Entry(frame_create, width=30, show="*")
entry_password.pack()

button_toggle_password = tk.Button(frame_create, text="👁", command=toggle_password)
button_toggle_password.pack()

button_save_new = tk.Button(frame_create, text="Save", command=save_credentials)
button_save_new.pack()

frame_saved_credentials = tk.Frame(frame_main)

frame_default = tk.Frame(root)
tk.Label(frame_default, text="Default Passwords Screen").pack()

root.mainloop()
