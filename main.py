import tkinter as tk
from PIL import Image,ImageTk

root = tk.Tk()

canvas = tk.Canvas(root, height=300, width=600)
canvas.grid(columnspan=3)

#logo
logo = Image.open('logo.png') 
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

root.mainloop()
