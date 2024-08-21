import bcrypt
import tkinter as tk
from tkinter import messagebox, Label
import subprocess
import os
import sys
from PIL import ImageTk, Image
import ctypes

users = {}

def create_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password

    with open('hash.txt', 'a') as file:
        file.write(f"{username}:{hashed_password.decode('utf-8')}\n")

def load_users():
    with open('hash.txt', 'r') as file:
        for line in file:
            username, hashed_password = line.strip().split(':')
            users[username] = hashed_password.encode('utf-8')

def login(username, password):
    if username in users:
        stored_password = users[username]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            messagebox.showinfo("Login", "Login successful!")
            open_dashboard_page()  # Redirect to the homepage
        else:
            messagebox.showerror("Login", "Incorrect password.")
    else:
        messagebox.showerror("Login", "User not found.")

def handle_signup():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        create_user(username, password)
        messagebox.showinfo("Signup", "User created successfully.")
    else:
        messagebox.showerror("Signup", "Please enter both username and password.")

def open_login_page():
    login_window = tk.Toplevel(window)
    login_window.title("Login Page")
    login_window.geometry("500x500")  # Set the desired window size

    background_label = Label(login_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window with the image

    # Create and position GUI elements for the login page
    login_username_label = tk.Label(login_window, text="Username:")
    login_username_label.pack(anchor="center")

    login_username_entry = tk.Entry(login_window)
    login_username_entry.pack(anchor="center")

    login_password_label = tk.Label(login_window, text="Password:")
    login_password_label.pack(anchor="center")

    login_password_entry = tk.Entry(login_window, show="*")
    login_password_entry.pack(anchor="center")

    login_button = tk.Button(login_window, text="Log In", command=lambda: login(login_username_entry.get(), login_password_entry.get()))
    login_button.pack(anchor="center")

    # Center the login page in the window
    login_window.update_idletasks()
    width = login_window.winfo_width()
    height = login_window.winfo_height()
    x = (login_window.winfo_screenwidth() // 2) - (width // 2)
    y = (login_window.winfo_screenheight() // 2) - (height // 2)
    login_window.geometry(f"{width}x{height}+{x}+{y}")

def handle_login():
    open_login_page()

def open_dashboard_page():
    # Close the current window
    window.destroy()
    # Start the homepage window
    subprocess.Popen([sys.executable, "HomePage.py"])

# Create the main window
window = tk.Tk()
window.title("Payroll Management System")
window.geometry("500x500")  # Set the desired window size

# Retrieve screen resolution
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Resize the image to match the screen resolution
background_image = Image.open("payroll1.webp")
background_image = background_image.resize((screen_width, screen_height), Image.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

# Set the background image for the main window
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window with the image

# Create and position GUI elements
title_label = tk.Label(window, text="Payroll Management System", font=("Century Gothic", 50, "bold"), fg="brown")
title_label.pack(anchor="center",pady=100)

username_label = tk.Label(window, text="Username:")
username_label.pack(anchor="center",pady=10)

username_entry = tk.Entry(window)
username_entry.pack(anchor="center",pady=10)

password_label = tk.Label(window, text="Password:")
password_label.pack(anchor="center",pady=10)

password_entry = tk.Entry(window, show="*")
password_entry.pack(anchor="center",pady=10)

signup_button = tk.Button(window, text="Sign Up", command=handle_signup)
signup_button.pack(anchor="center",pady=10)

login_button = tk.Button(window, text="Log In", command=handle_login)
login_button.pack(anchor="center",pady=10)

# Load user data from file
load_users()

# Center the main window
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (window_width // 2)
y = (window.winfo_screenheight() // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Start the main GUI event loop
window.mainloop()
