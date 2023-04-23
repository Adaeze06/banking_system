import tkinter as tk
from PIL import Image,ImageTk
import os 
import mysql.connector
from tkinter import messagebox

db = mysql.connector.connect(
    user="root",
    password="Frederick$01",
    database="elite_savings"
)
cursor = db.cursor()

root = tk.Tk()


#window setup
canvas = tk.Canvas(root, height=300, width=600)
canvas.grid(columnspan=3, rowspan=3)

#logo
logo = Image.open('logo.png') 
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#instructions
instructions = tk.Label(root, text = "Welcome to Elite Savings! Click a button to begin.")
instructions.grid(columnspan=3, column=0, row=1)


#function for Registering New User
def create_account():
    top = tk.Toplevel(root)
    top.title("Create New Account")
    top.geometry("500x500")
    label = tk.Label(top, image=logo)
    label2 = tk.Label(top, text="To create a new account enter details below!")
    label.pack(pady=20)
    label2.pack(pady=20)

    # Entries
    username_frame = tk.Frame(top)
    username_label = tk.Label(username_frame, text="Username:")
    username_label.pack(side="left")
    username_entry = tk.Entry(username_frame)
    username_entry.pack(side="left")
    username_frame.pack(pady=10)

    password_frame = tk.Frame(top)
    password_label = tk.Label(password_frame, text="Password:")
    password_label.pack(side="left")
    password_entry = tk.Entry(password_frame, show="*")
    password_entry.pack(side="left")
    password_frame.pack(pady=10)

    # Submit Button
    def submit():
        # Insert data into MySQL table
        username = username_entry.get()
        password = password_entry.get()
        cursor.execute("INSERT INTO elite_users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        messagebox.showinfo("Success", "New user account created!")
        top.destroy()

    submit_button = tk.Button(top, text="Submit", command=submit)
    submit_button.pack(pady=10)

def log_in():
    top = tk.Toplevel(root)
    top.title('Log In')
    top.geometry('500x500')
    label3 = tk.Label(top, image=logo)
    label4 = tk.Label(top, text="To login enter details below!")
    label3.pack(pady=20)
    label4.pack(pady=20)

    # Username Entry
    username_frame = tk.Frame(top)
    username_label = tk.Label(username_frame, text="Username:")
    username_label.pack(side="left")
    username_entry = tk.Entry(username_frame)
    username_entry.pack(side="left")
    username_frame.pack(pady=10)

    # Password Entry
    password_frame = tk.Frame(top)
    password_label = tk.Label(password_frame, text="Password:")
    password_label.pack(side="left")
    password_entry = tk.Entry(password_frame, show="*")
    password_entry.pack(side="left")
    password_frame.pack(pady=10)

    # Submit Button
    def submit():
        # Retrieve username and password from entries
        username = username_entry.get()
        password = password_entry.get()

        # Check if user exists in MySQL table
        cursor.execute("SELECT * FROM elite_users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    submit_button = tk.Button(top, text="Submit", command=submit)
    submit_button.pack(pady=10)
    

#login button
login_text=tk.StringVar()
login_btn=tk.Button(root, textvariable= login_text, command=lambda:log_in(), bg= '#fc9484', fg='white', height=2, width=15)
login_text.set('Login')
login_btn.grid(column=1, row=2)

#register button
register_text=tk.StringVar()
register_btn=tk.Button(root, textvariable= register_text, command=lambda:create_account(), bg= '#fc9484', fg='white', height=2, width=15)
register_text.set('Create Account')
register_btn.grid(column=1, row=3)

# Create check balance button
balance_text=tk.StringVar()
balance_btn=tk.Button(root, textvariable= balance_text, command=lambda:check_balance(), bg= '#fc9484', fg='white', height=2, width=15)
balance_text.set('Check Balance')
balance_btn.grid(column=1, row=4)

# Add check balance button to frame
def check_balance():
    # Retrieve balance from MySQL table
    username = "Samantha"  # Replace with logged-in user's username
    cursor.execute("SELECT balance FROM elite_users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        messagebox.showinfo("Balance", f"Your current balance is: ${balance}")
    else:
        messagebox.showerror("Error", "Could not retrieve balance.")





root.mainloop()
