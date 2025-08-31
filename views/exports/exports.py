import tkinter as tk
import tkinter.messagebox as messagebox 
from tkinter import ttk, filedialog

from ..colors import *
from ..header import header

from global_values import *

from services.tools import set_image
from services.csv_importer_service import prepare_params
from services.csv_export_service import transactions_export


from repository.user_repository import list_users

def exports_init(main_frame, args=None):
  header(main_frame, 'Exportações', 'icons/icon-export.png')

  frame_body = tk.Frame(main_frame, width=body_width, height=body_height, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=footer_width, height=footer_height, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  csv(frame_body)

def csv(frame):
  l_title = tk.Label(frame, text='Exportar CSV', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_title.place(x=20, y=5)

  input_user(frame)
  export_button(frame)

def input_user(frame):
  global users_combobox

  l_user = tk.Label(frame, text='Usuário', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_user.place(x=20, y=35)

  global list_userss
  list_userss = list_users()

  users = [user.name for user in list_userss]

  users_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  users_combobox['values'] = (users)
  users_combobox.place(x=170, y=35)

def export_button(frame):
  global btn_export
  btn_export = tk.Button(frame, text="Exportar CSV", command=action_export)
  btn_export.place(x=20, y=65)

def action_export():
  user_name = users_combobox.get()

  if not user_name:
    messagebox.showwarning("Atenção", "Nome do usuário não pode estar vazio.")
    return

  user_id =  next((user.id for user in list_userss if user.name == user_name), None)

  if not user_id:
    messagebox.showwarning("Atenção", "Usuário não se encontra na lista.")
    return

  transactions_export(user_id)