import tkinter as tk
import tkinter.messagebox as messagebox 
from tkinter import ttk

from ..colors import *
from ..header import header

from global_values import *

from services.tools import set_image

from components.mult_select_obj_v2 import MultiSelectCombobox

from repository.payment_repository import list_payments_by_bank_account_id, list_payments_by_user_id, delete_payments_by_bank_account_id
from repository.transaction_repository import list_transactions_values_expenses_to_categories
from repository.user_repository import list_users
from repository.bank_account_repository import list_banks_and_users, create_bank_account, update_bank, delete_bank


current_selected_item = None

def banks_init(main_frame, args=None):
  header(main_frame, 'Instituições Financeiras (Bancos)', 'icons/icon-bank.png')

  frame_body = tk.Frame(main_frame, width=body_width, height=body_height, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=footer_width, height=footer_height, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  tab(frame_body)
  input_filter_users(frame_body)
  button_search(frame_body)

  input_name(frame_footer)
  input_user(frame_footer)

  button_create(frame_footer)
  button_edit(frame_footer)
  button_destroy(frame_footer)


# >>>>>>>>>>>>>
# TABELA ACTION
# >>>>>>>>>>>>>

def tab(frame):
  tab_head = ['#Id', 'Instituição', 'Usuário']

  global tree

  tree = ttk.Treeview(frame, selectmode="extended",columns=tab_head, show="headings")

  vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
  
  hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

  tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

  tree.grid(column=0, row=0, sticky='nsew', padx=(150, 5), pady=5)
  vsb.grid(column=1, row=0, sticky='ns', padx=(0, 5), pady=5)

  hd=["center","w", "w"]
  h=[30,400,100]
  n=0

  for col in tab_head:
    tree.heading(col, text=col.title(), anchor=tk.CENTER)      
    tree.column(col, width=h[n],anchor=hd[n])    
    n+=1
  
  seed_table()

  tree.bind("<<TreeviewSelect>>", on_tree_select)

def seed_table(user_ids=None):
  list_banks = list_banks_and_users(user_ids)

  lista_itens = [
    (
      bank.id,                     
      bank.name,
      bank.user_name
    )
    for bank in list_banks
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

# >>>>>>>>>>>>
# FILTER USERS
# >>>>>>>>>>>>

def input_filter_users(frame, inicial_values=None):
  global users_filter_combobox

  coo_x = 750

  l_users_filter = tk.Label(frame, text='Filtro por Usuários', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_users_filter.place(x=coo_x, y=10)

  users = list_users()

  users_filter_combobox = MultiSelectCombobox(frame, objects=users, display_property="name", value_property="id", initial_values=inicial_values, width=11)
  users_filter_combobox.place(x=coo_x, y=40)

def button_search(frame):
  global filter_img
  filter_img = set_image('icons/icon-search.png', 17, 17)

  buttom = tk.Button(frame, command=seach_action, image=filter_img, text='Busca'.upper(), width=70, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=750, y=70)

def seach_action():
  users = users_filter_combobox.get_selected_values()

  for item in tree.get_children():
      tree.delete(item)
      
  seed_table(users)

# >>>>>>>>>>>>>
# CREATE ACTION
# >>>>>>>>>>>>>

def input_name(frame):
  global i_name

  l_name = tk.Label(frame, text='None da Instiuição', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_name.place(x=20, y=20)

  i_name = tk.Entry(frame, width=12, justify=tk.LEFT, relief=tk.SOLID)
  i_name.place(x=150, y=20)

def input_user(frame):
  global users_combobox

  l_user = tk.Label(frame, text='Usuário', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_user.place(x=20, y=60)

  global list_userss
  list_userss = list_users()

  users = [user.name for user in list_userss]

  users_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  users_combobox['values'] = (users)
  users_combobox.place(x=150, y=60)

def button_create(frame):
  global add_img
  add_img = set_image('icons/icon-plus.png', 17, 17)

  global create_buttom
  create_buttom = tk.Button(frame, command=action_create, image=add_img, text='Adicionar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  create_buttom.place(x=20, y=110)

def action_create():
  bank_name = i_name.get().strip()
  user_name = users_combobox.get()

  if not bank_name:
    messagebox.showwarning("Atenção", "O nome da instituição não pode estar vazio.")
    return
  
  if not user_name:
    messagebox.showwarning("Atenção", "Deve-se selecionar um usuário.")
    return

  user_id = next((user.id for user in list_userss if user.name == user_name), None)

  if not user_id:
    messagebox.showwarning("Atenção", "Usuário não percente a lista")
    return  
 
  try:
    new_bank = create_bank_account(bank_name, user_id)
    print(f"Instituição '{bank_name}' criada com sucesso.")
  except Exception as e:
    print(f"Erro ao criar a categoria: {e}")
    return
  
  users_combobox.delete(0, 'end')
  i_name.delete(0, tk.END)

  item = (new_bank.id, new_bank.name, user_name)

  add_item_table(item)

# >>>>>>>>>>>
# EDIT ACTION
# >>>>>>>>>>>

def button_edit(frame):
  global edit_img
  edit_img = set_image('icons/icon-edit.png', 17, 17)

  global edit_button
  edit_button = tk.Button(frame, command=action_edit, image=edit_img, text='Editar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  edit_button.place(x=130, y=110)

def action_edit():
  global current_selected_item

  selected_item = tree.selection()
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione uma instituição antes de editar.")
    return

  current_selected_item = selected_item[0]

  values = tree.item(current_selected_item, 'values')
  if values:
    i_name.delete(0, tk.END)
    i_name.insert(0, values[1])

  edit_button.config(text='Salvar'.upper(), command=action_update)
  users_combobox.config(state=tk.DISABLED)
  create_buttom.config(state=tk.DISABLED)
  destroy_button.config(state=tk.DISABLED)

def action_update():
  global current_selected_item

  new_name = i_name.get().strip()

  if not new_name:
    messagebox.showwarning("Atenção", "O nome da instituição não pode estar vazio.")
    return

  line = tree.item(current_selected_item, 'values')

  bank_id = line[0]

  user_name = line[2]

  update_bank(bank_id, new_name)

  tree.item(current_selected_item, values=(bank_id, new_name, user_name))

  i_name.delete(0, tk.END)

  reset_edit_mode()

def reset_edit_mode():
    edit_button.config(text='Editar'.upper(), command=action_edit)
    users_combobox.config(state=tk.NORMAL)
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
  destroy_button.place(x=240, y=110)

def destroy():
  selected_item = tree.selection()  
  
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione um banco.")
    return

  bank_id = int(tree.item(selected_item, 'values')[0])  

  payments = list_payments_by_bank_account_id(bank_id)

  payment_ids = [payment.id for payment in payments]

  if payment_ids and transaction_exists(payment_ids):
    messagebox.showwarning("Atenção", "Banco possui transações")
    return

  if payment_ids:
    delete_payments_by_bank_account_id(payment_ids)

  delete_bank(bank_id)

  tree.delete(selected_item)

def transaction_exists(payment_ids):
  objects = list_transactions_values_expenses_to_categories(None, None, None, None, payment_ids)
  return True if len(objects) > 0 else False