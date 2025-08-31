import tkinter as tk
import tkinter.messagebox as messagebox 
from tkinter import ttk

from ..colors import *
from ..header import header

from global_values import *

from services.tools import set_image

from repository.payment_repository import create_payment, delete_payments_by_user_id
from repository.transaction_repository import list_transactions_values_expenses_to_categories
from repository.user_repository import list_users, create_user, update_user, delete_user

from models.payment import TypeRole

current_selected_item = None

def users_init(main_frame, args=None):
  header(main_frame, 'Usuários', 'icons/icon-users.png')

  frame_body = tk.Frame(main_frame, width=body_width, height=body_height, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=footer_width, height=footer_height, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  tab(frame_body)

  input_name(frame_footer)

  button_create(frame_footer)

  button_edit(frame_footer)

  button_destroy(frame_footer)

# >>>>>>>>>>>>>
# TABELA ACTION
# >>>>>>>>>>>>>

def tab(frame):
  tab_head = ['#Id', 'None']

  global tree

  tree = ttk.Treeview(frame, selectmode="extended",columns=tab_head, show="headings")

  vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
  
  hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

  tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

  # Adicionando a Treeview e as Scrollbars ao layout com margens
  tree.grid(column=0, row=0, sticky='nsew', padx=(150, 5), pady=5)    # Margens internas
  vsb.grid(column=1, row=0, sticky='ns', padx=(0, 5), pady=5)  # Margem direita

  hd=["center","w"]
  h=[30,400]
  n=0

  for col in tab_head:
    tree.heading(col, text=col.title(), anchor=tk.CENTER)      
    tree.column(col, width=h[n],anchor=hd[n])    
    n+=1
  
  seed_table()

  tree.bind("<<TreeviewSelect>>", on_tree_select)

def seed_table():
  users = list_users()

  lista_itens = [
    (
        user.id,                     
        user.name
    )
    for user in users
  ]

  for item in lista_itens:
    add_item_table(item)

def add_item_table(item):
  item_id = tree.insert('', 'end', values=item)

def on_tree_select(event):
  global current_selected_item

  selected_item = tree.selection()

  if not selected_item:
    return

  if selected_item[0] != current_selected_item:
      current_selected_item = selected_item[0]
      reset_edit_mode()

      values = tree.item(current_selected_item, 'values')
      if values:
        i_name.delete(0, tk.END)

# >>>>>>>>>>>>>
# CREATE ACTION
# >>>>>>>>>>>>>

def input_name(frame):
  global i_name

  l_name = tk.Label(frame, text='Nome', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_name.place(x=20, y=20)

  i_name = tk.Entry(frame, width=12, justify=tk.LEFT, relief=tk.SOLID)
  i_name.place(x=120, y=20)

def button_create(frame):
  global add_img
  add_img = set_image('icons/icon-plus.png', 17, 17)

  global create_buttom
  create_buttom = tk.Button(frame, command=action_create, image=add_img, text='Adicionar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  create_buttom.place(x=20, y=70)

def action_create():
  user_name = i_name.get().strip()

  if not user_name:
    messagebox.showwarning("Atenção", "O nome do usuário não pode estar vazio.")
    return
   
  try:
    new_user = create_user(user_name)
    print(f"Usuário '{user_name}' criada com sucesso.")
  except Exception as e:
    print(f"Erro ao criar a categoria: {e}")
    return
  
  create_payment(TypeRole.DINHEIRO.value, TypeRole.DINHEIRO.value, new_user.id)

  i_name.delete(0, tk.END)

  item = (new_user.id, new_user.name)

  add_item_table(item)

# >>>>>>>>>>>
# EDIT ACTION
# >>>>>>>>>>>

def button_edit(frame):
  global edit_img
  edit_img = set_image('icons/icon-edit.png', 17, 17)

  global edit_button
  edit_button = tk.Button(frame, command=action_edit, image=edit_img, text='Editar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  edit_button.place(x=130, y=70)

def action_edit():
  global current_selected_item

  selected_item = tree.selection()
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione um usuário antes de editar.")
    return

  current_selected_item = selected_item[0]

  values = tree.item(current_selected_item, 'values')
  if values:
    i_name.delete(0, tk.END)
    i_name.insert(0, values[1])

  edit_button.config(text='Salvar'.upper(), command=action_update)
  create_buttom.config(state=tk.DISABLED)
  destroy_button.config(state=tk.DISABLED)

def action_update():
  global current_selected_item

  new_name = i_name.get().strip()

  if not new_name:
    messagebox.showwarning("Atenção", "O nome não pode estar vazio.")
    return

  user_id = tree.item(current_selected_item, 'values')[0]

  update_user(user_id, new_name)

  tree.item(current_selected_item, values=(user_id, new_name))

  i_name.delete(0, tk.END)

  reset_edit_mode()

def reset_edit_mode():
    edit_button.config(text='Editar'.upper(), command=action_edit)
    create_buttom.config(state=tk.NORMAL)
    destroy_button.config(state=tk.NORMAL)

# >>>>>>>>>>>>>>
# DESTROY ACTION
# >>>>>>>>>>>>>>

def button_destroy(frame):
  global trash_img
  trash_img = set_image('icons/icon-trash.png', 17, 17)

  global destroy_button
  destroy_button = tk.Button(frame, command=destroy, image=trash_img, text='Apagar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  destroy_button.place(x=240, y=70)

def destroy():
  selected_item = tree.selection()  
  
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione um usuário.")
    return

  id = tree.item(selected_item, 'values')[0]

  if transaction_exists(id):
    messagebox.showwarning("Atenção", "Usuário possui transações")
    return

  delete_payments_by_user_id(id)
  delete_user(id)

  tree.delete(selected_item)

def transaction_exists(id):
  objects = list_transactions_values_expenses_to_categories(None, None, [id], None)
  return True if len(objects) > 0 else False
