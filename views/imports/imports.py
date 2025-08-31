import tkinter as tk
import tkinter.messagebox as messagebox 
from tkinter import ttk, filedialog

from ..colors import *
from ..header import header

from global_values import *

from services.tools import set_image
from services.csv_importer_service import prepare_params
from services.csv_export_service import model_export

from repository.user_repository import list_users

def imports_init(main_frame, args=None):
  header(main_frame, 'Importações', 'icons/icon-import.png')

  frame_body = tk.Frame(main_frame, width=body_width, height=body_height, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=footer_width, height=footer_height, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  csv(frame_body)

def csv(frame):
  l_title = tk.Label(frame, text='Importa CSV', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_title.place(x=20, y=5)

  input_user(frame)
  input_file(frame)
  input_model(frame)

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

def input_file(frame):
  global btn_import
  btn_import = tk.Button(frame, text="Importar CSV", command=get_csv_file)
  btn_import.place(x=20, y=65)

  global l_file_name
  l_file_name = tk.Label(frame, text='', height=1, anchor=tk.NW, font=('Ivy 12'), bg=co1, fg=co4)
  l_file_name.place(x=170, y=65)

def get_csv_file():
  global csv_file
  csv_file = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])

  file_name = csv_file.split('/')[-1]

  l_file_name.config(text=file_name)

  btn_import.config(text='Salvar'.upper(), command=import_csv_file)

def import_csv_file():
  user_name = users_combobox.get()

  if not user_name:
    messagebox.showwarning("Atenção", "Nome do usuário não pode estar vazio.")
    return

  user_id =  next((user.id for user in list_userss if user.name == user_name), None)

  if not user_id:
    messagebox.showwarning("Atenção", "Usuário não se encontra na lista.")
    return

  result = prepare_params(csv_file, user_id)

  l_file_name.config(text='')
  btn_import.config(text='Importar CSV'.upper(), command=get_csv_file)

  if isinstance(result, str):
    messagebox.showwarning("ERRO", result)    
  else:
    messagebox.showinfo("Sucesso", f"{len(result)} transações importadas!")

def input_model(frame):
  global btn_model
  btn_model = tk.Button(frame, text="Modelo CSV", command=model_export)
  btn_model.place(x=20, y=100)





