#import all necessary modules

import tkinter as tk
from PIL import Image,ImageTk
import os 
import mysql.connector
from tkinter import messagebox
from tkinter import simpledialog

#connect to my sql database

db = mysql.connector.connect(
    user="root",
    password="Frederick$01",
    database="elite_savings"
)
cursor = db.cursor()


root = tk.Tk()


# main window setup
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


#function for registering new user
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

    balance_frame = tk.Frame(top)
    balance_label = tk.Label(balance_frame, text = "Starting Balance:")
    balance_label.pack(side="left")
    balance_entry = tk.Entry(balance_frame)
    balance_entry.pack(side="left")
    balance_frame.pack(pady=10)

    # Submit Button
    def submit():
        # Insert data into MySQL table
        username = username_entry.get()
        password = password_entry.get()
        balance = balance_entry.get()
        cursor.execute("INSERT INTO elite_users (username, password, balance) VALUES (%s, %s, %s)", (username, password, balance))
        db.commit()
        messagebox.showinfo("Success", "New user account created!")
        top.destroy()

    submit_button = tk.Button(top, text="Submit", command=submit)
    submit_button.pack(pady=10)

#function for logging users in
def log_in():
    top = tk.Toplevel(root)
    top.title('Log In')
    top.geometry('500x500')
    label3 = tk.Label(top, image=logo)
    label4 = tk.Label(top, text="To login enter details below!")
    label3.pack(pady=20)
    label4.pack(pady=20)

    #entries
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

    #submit Button
    def submit():
        #retrieve username and password from entries
        username = username_entry.get()
        password = password_entry.get()

        #check if user exists in MySQL table
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

#check balance button
balance_text=tk.StringVar()
balance_btn=tk.Button(root, textvariable= balance_text, command=lambda:check_balance(), bg= '#fc9484', fg='white', height=2, width=15)
balance_text.set('Check Balance')
balance_btn.grid(column=1, row=4)

#withdraw button
withdraw_text=tk.StringVar()
withdraw_btn=tk.Button(root, textvariable= withdraw_text, command=lambda:withdraw_money(), bg= '#fc9484', fg='white', height=2, width=15)
withdraw_text.set('Withdraw Money')
withdraw_btn.grid(column=1, row=5)

#deposit button 
deposit_text=tk.StringVar()
deposit_btn=tk.Button(root, textvariable= deposit_text, command=lambda:deposit_money(), bg= '#fc9484', fg='white', height=2, width=15)
deposit_text.set('Deposit Money')
deposit_btn.grid(column=1, row=6)

#function for checking account balance
def check_balance():
  
    #ask for username and password
    username = simpledialog.askstring("Check Balance", "Enter your username:")
    password = simpledialog.askstring("Check Balance", "Enter your password:", show="*")

    #check if user exists and password is correct
    cursor.execute("SELECT * FROM elite_users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Error", "Invalid username or password.")
        return

    #retrieve balance from MySQL table    
    if result:
        balance = result[5] # balance is the fifth column in the table 
        messagebox.showinfo("Balance", f"Your current balance is: ${balance}")
    else:
        messagebox.showerror("Error", "Could not retrieve balance.")
   
#function for allowing users to withdraw money
def withdraw_money():
    #ask for username and password
    username = simpledialog.askstring("Withdraw Money", "Enter your username:")
    password = simpledialog.askstring("Withdraw Money", "Enter your password:", show="*")

    #check if user exists and password is correct
    cursor.execute("SELECT * FROM elite_users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Error", "Invalid username or password.")
        return

    #retrieve balance from MySQL table
    balance = result[5] # balance is the fifth column in the table 

    #ask for withdraw amount
    withdraw_amount = simpledialog.askinteger("Withdraw Money", f"Your current balance is: ${balance}. How much would you like to withdraw?")
    if not withdraw_amount:
        #user cancelled the dialog box
        return

    # check if balance is sufficient
    if balance < withdraw_amount:
        messagebox.showerror("Error", "Insufficient balance.")
        return

    #deduct withdraw_amount from balance
    new_balance = balance - withdraw_amount

    #update balance in MySQL table
    cursor.execute("UPDATE elite_users SET balance = %s WHERE username = %s", (new_balance, username))
    db.commit()

    #show confirmation message
    messagebox.showinfo("Withdraw Money", f"Withdrawal successful! Your new balance is: ${new_balance}")


#function for allowing users to deposit money
def deposit_money():
    #ask for username and password
    username = simpledialog.askstring("Withdraw Money", "Enter your username:")
    password = simpledialog.askstring("Withdraw Money", "Enter your password:", show="*")

    #check if user exists and password is correct
    cursor.execute("SELECT * FROM elite_users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Error", "Invalid username or password.")
        return

    #retrieve balance from MySQL table
    balance = result[5] # balance is the fifth column in the table 

    #ask for deposit amount
    deposit_amount = simpledialog.askinteger("Deposit Money", f"Your current balance is: ${balance}. How much would you like to deposit?")
    if not deposit_amount:
        #user cancelled the dialog box
        return

    #add deposit_amount from balance
    new_balance = balance + deposit_amount

    #update balance in MySQL table
    cursor.execute("UPDATE elite_users SET balance = %s WHERE username = %s", (new_balance, username))
    db.commit()

    #show confirmation message
    messagebox.showinfo("Deposit Money", f"Deposit successful! Your new balance is: ${new_balance}")

root.mainloop()
