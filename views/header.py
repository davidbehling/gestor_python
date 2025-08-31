import tkinter as tk
from tkinter import ttk

from .colors import *
from services.tools import set_image

def header(main_frame, text, icon):
  frame_header = tk.Frame(main_frame, width=1043, height=50, bg=co1, relief='flat')
  frame_header.grid(row=0, column=0)

  global log_img
  log_img = set_image(icon, 45, 45)

  label_image = tk.Label(frame_header, image=log_img, text=f' {text}', width=900, compound=tk.LEFT, padx=5, relief=tk.RAISED, anchor=tk.NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
  label_image.place(x=0, y=0)