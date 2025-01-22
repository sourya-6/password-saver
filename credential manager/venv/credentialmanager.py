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
    
    fake_credentials = {
        "Social": {"username": "fake_user", "password": "fakepass"},
        "Game": {"username": "gamer123", "password": "gamepass"}
    }
    if not os.path.exists("fake_credentials.json"):
        with open("fake_credentials.json", "w") as f:
            json.dump(fake_credentials, f, indent=4)

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
            show_saved_passwords_fake()

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

# Function to display real stored credentials one at a time
def show_saved_passwords_real():
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
        messagebox.showinfo("No Data", "No real credentials saved yet.")
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
    
    next_button = tk.Button(frame_saved_credentials, text='➡', command=show_next_password_real)
    next_button.grid(row=0, column=4, padx=5, pady=5)
    
    frame_saved_credentials.pack(fill=tk.BOTH, expand=True)

# Function to display fake stored credentials one at a time
def show_saved_passwords_fake():
    global current_index
    for widget in frame_saved_credentials.winfo_children():
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

    title = keys[current_index]
    creds = credentials[title]
    
    tk.Label(frame_saved_credentials, text=title, width=20).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame_saved_credentials, text=creds['username'], width=20).grid(row=0, column=1, padx=5, pady=5)
    
    password_entry = tk.Entry(frame_saved_credentials, width=20, show='*')
    password_entry.insert(0, creds['password'])
    password_entry.grid(row=0, column=2, padx=5, pady=5)
    
    toggle_button = tk.Button(frame_saved_credentials, text='👁', command=lambda: toggle_password(password_entry, toggle_button))
    toggle_button.grid(row=0, column=3, padx=5, pady=5)
    
    next_button = tk.Button(frame_saved_credentials, text='➡', command=show_next_password_fake)
    next_button.grid(row=0, column=4, padx=5, pady=5)
    
    frame_saved_credentials.pack(fill=tk.BOTH, expand=True)

# Function to create a new password for real credentials
def create_new_password_real():
    create_new_password(fake=False)

# Function to create a new password for fake credentials
def create_new_password_fake():
    create_new_password(fake=True)

# Generic function to create a new password
def create_new_password(fake=False):
    def save_new_password():
        title = entry_title.get().strip()
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        
        if not title or not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        filename = "fake_credentials.json" if fake else "credentials.json"
        
        if os.path.exists(filename):
            with open(filename, "r") as f:
                credentials = json.load(f)
        else:
            credentials = {}
        
        credentials[title] = {"username": username, "password": password}
        
        with open(filename, "w") as f:
            json.dump(credentials, f, indent=4)
        
        messagebox.showinfo("Success", "Password saved successfully!")
        new_password_window.destroy()
        if fake:
            show_saved_passwords_fake()
        else:
            show_saved_passwords_real()
    
    new_password_window = tk.Toplevel(root)
    new_password_window.title("Create New Password")
    
    tk.Label(new_password_window, text="Title:").grid(row=0, column=0)
    entry_title = tk.Entry(new_password_window)
    entry_title.grid(row=0, column=1)
    
    tk.Label(new_password_window, text="Username:").grid(row=1, column=0)
    entry_username = tk.Entry(new_password_window)
    entry_username.grid(row=1, column=1)
    
    tk.Label(new_password_window, text="Password:").grid(row=2, column=0)
    entry_password = tk.Entry(new_password_window, show="*")
    entry_password.grid(row=2, column=1)
    
    tk.Button(new_password_window, text="Save", command=save_new_password).grid(row=3, columnspan=2)

# Function to show next real password
def show_next_password_real():
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
    
    show_saved_passwords_real()

# Function to show next fake password
def show_next_password_fake():
    global current_index
    if os.path.exists("fake_credentials.json"):
        with open("fake_credentials.json", "r") as f:
            credentials = json.load(f)
    else:
        credentials = {}
    
    if current_index < len(credentials) - 1:
        current_index += 1
    else:
        current_index = 0
    
    show_saved_passwords_fake()

root = tk.Tk()
root.title("Password Manager")
root.geometry("600x500")

frame_passkey = tk.Frame(root)
frame_passkey.pack()

label_passkey = tk.Label(frame_passkey, text="Enter Passkey:")
label_passkey.pack()
entry_passkey = tk.Entry(frame_passkey, width=10, show="*")
entry_passkey.pack()
button_submit_passkey = tk.Button(frame_passkey, text="Submit", command=check_passkey)
button_submit_passkey.pack()

frame_main = tk.Frame(root)
button_create_new = tk.Button(frame_main, text="Create New (Real)", command=create_new_password_real)
button_create_new.pack()
button_show_saved = tk.Button(frame_main, text="Show Saved (Real)", command=show_saved_passwords_real)
button_show_saved.pack()
button_exit = tk.Button(frame_main, text="Exit", command=exit_application)
button_exit.pack()
frame_saved_credentials = tk.Frame(frame_main)

frame_default = tk.Frame(root)
button_create_default = tk.Button(frame_default, text="Create New (Fake)", command=create_new_password_fake)
button_create_default.pack()
button_show_default = tk.Button(frame_default, text="Show Saved (Fake)", command=show_saved_passwords_fake)
button_show_default.pack()
button_exit_default = tk.Button(frame_default, text="Exit", command=exit_application)
button_exit_default.pack()
frame_saved_credentials.pack()

load_default_credentials()
root.mainloop()
