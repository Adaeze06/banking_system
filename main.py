import tkinter as tk
from PIL import Image,ImageTk
import os 

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
instructions = tk.Label(root, text = "Welcome to Elite Savings!  Enter your Account Number to log in.")
instructions.grid(columnspan=3, column=0, row=1)

#buttons
register_text=tk.StringVar()
register_btn=tk.Button(root, textvariable= register_text, bg= '#FF99AC', fg='white', height=2, width=15)
register_text.set('Register')
register_btn.grid(column=1, row=2)

canvas = tk.Canvas(root, height=2500, width=600)
canvas.grid(columnspan=3)

root.mainloop()
