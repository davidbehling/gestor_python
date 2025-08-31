import tkinter as tk
import tkinter.messagebox as messagebox 
from tkinter import ttk

from ..colors import *
from ..header import header

from global_values import *

from services.tools import set_image, is_valid_day

from components.mult_select_obj_v2 import MultiSelectCombobox

from models.payment import TypeRole

from repository.bank_account_repository import list_bank_accounts
from repository.payment_repository import list_payments, create_payment, update_payment, delete_payment
from repository.transaction_repository import list_transactions_values_expenses_to_categories
from repository.user_repository import list_users

current_selected_item = None

def payments_init(main_frame, args=None):
  header(main_frame, 'Tipos de Pagamentos', 'icons/icon-type-payments.png')

  frame_body = tk.Frame(main_frame, width=body_width, height=body_height, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=footer_width, height=footer_height, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  tab(frame_body)
  input_filter_users(frame_body)
  button_search(frame_body)

  input_user(frame_footer)
  input_description(frame_footer)
  input_type(frame_footer)
  input_close_day(frame_footer)
  input_due_day(frame_footer)
  input_bank(frame_footer)

  button_create(frame_footer)

  button_edit(frame_footer)

  button_destroy(frame_footer)
  
  update_due_day_fields()

# >>>>>>>>>>>>>
# TABELA ACTION
# >>>>>>>>>>>>>

def tab(frame):
  tab_head = ['#Id', 'Descrição', 'Tipo', 'Fechamento', 'Vencimento', 'Banco', 'Usuário']

  global tree

  tree = ttk.Treeview(frame, selectmode="extended",columns=tab_head, show="headings")

  vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
  
  hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

  tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

  # Adicionando a Treeview e as Scrollbars ao layout com margens
  tree.grid(column=0, row=0, sticky='nsew', padx=(5, 5), pady=5)    # Margens internas
  vsb.grid(column=1, row=0, sticky='ns', padx=(0, 5), pady=5)  # Margem direita
  # hsb.grid(column=0, row=1, sticky='ew', padx=5, pady=(0, 5)) 

  hd=["center","w","w","w","w","w","w"]
  h=[30,130,100,100,100,100,100]
  n=0

  for col in tab_head:
    tree.heading(col, text=col.title(), anchor=tk.CENTER)      
    tree.column(col, width=h[n],anchor=hd[n])    
    n+=1
  
  seed_table()

  tree.bind("<<TreeviewSelect>>", on_tree_select)

def seed_table(user_ids=None):
  payments = list_payments(user_ids)

  lista_itens = [
    (
        payment.id,                     
        payment.name,
        payment.type,
        f"Dia {payment.closed_day}" if payment.closed_day else "",
        f"Dia {payment.due_day}" if payment.due_day else "",        
        payment.bank_account_name if payment.bank_account_name else "",
        payment.user_name
    )
    for payment in payments
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

      

# >>>>>>>>>>>>
# FILTER USERS
# >>>>>>>>>>>>

def input_filter_users(frame, inicial_values=None):
  global users_filter_combobox

  coo_x = 730

  l_users_filter = tk.Label(frame, text='Filtro por Usuários', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_users_filter.place(x=coo_x, y=10)

  users = list_users()

  users_filter_combobox = MultiSelectCombobox(frame, objects=users, display_property="name", value_property="id", initial_values=inicial_values, width=11)
  users_filter_combobox.place(x=coo_x, y=40)

def button_search(frame):
  global filter_img
  filter_img = set_image('icons/icon-search.png', 17, 17)

  buttom = tk.Button(frame, command=seach_action, image=filter_img, text='Busca'.upper(), width=70, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=730, y=70)

def seach_action():
  users = users_filter_combobox.get_selected_values()

  for item in tree.get_children():
      tree.delete(item)
      
  seed_table(users)

# >>>>>>>>>>>>>
# CREATE ACTION
# >>>>>>>>>>>>>

def input_user(frame):
  global users_combobox

  l_user = tk.Label(frame, text='Usuário', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_user.place(x=20, y=20)

  global list_userss
  list_userss = list_users()

  users = [user.name for user in list_userss]

  users_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  users_combobox['values'] = (users)
  users_combobox.place(x=150, y=20)

  users_combobox.bind("<<ComboboxSelected>>", update_bank_combobox_fields)

def input_description(frame):
  global i_description

  l_description = tk.Label(frame, text='Descrição', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_description.place(x=20, y=50)

  i_description = tk.Entry(frame, width=12, justify=tk.LEFT, relief=tk.SOLID)
  i_description.place(x=150, y=50)

def input_type(frame):
  global type_combobox

  l_type = tk.Label(frame, text='Tipo', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_type.place(x=20, y=80)

  global list_types
  list_types = [TypeRole.DINHEIRO.value, TypeRole.CREDITO.value, TypeRole.DEBITO.value, TypeRole.CREDIARIO.value]

  type_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  type_combobox['values'] = (list_types)
  type_combobox.place(x=150, y=80)

  type_combobox.bind("<<ComboboxSelected>>", update_due_day_fields)

def input_close_day(frame):
  global i_close_day

  l_close_day = tk.Label(frame, text='Dia de Fechamento', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_close_day.place(x=20, y=110)

  vcmd = (frame.register(is_valid_day), "%P")

  i_close_day = tk.Entry(frame, width=12, justify=tk.LEFT, relief=tk.SOLID,  validate="key", validatecommand=vcmd)
  i_close_day.place(x=150, y=110)

def input_due_day(frame):
  global i_due_day

  l_due_day = tk.Label(frame, text='Dia de Vencimento', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_due_day.place(x=20, y=140)

  vcmd = (frame.register(is_valid_day), "%P")

  i_due_day = tk.Entry(frame, width=12, justify=tk.LEFT, relief=tk.SOLID,  validate="key", validatecommand=vcmd)
  i_due_day.place(x=150, y=140)

def input_bank(frame):
  global bank_combobox

  l_bank = tk.Label(frame, text='Bancos', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_bank.place(x=20, y=170)

  bank_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  bank_combobox['values'] = ([])
  bank_combobox.place(x=150, y=170)

def update_due_day_fields(event=None):
  type_name = type_combobox.get()

  if type_name in [None, '', TypeRole.DINHEIRO.value]:
    i_close_day.delete(0, tk.END)
    i_due_day.delete(0, tk.END)
    bank_combobox.delete(0, tk.END)

    i_close_day.config(state=tk.DISABLED)
    i_due_day.config(state=tk.DISABLED)
    bank_combobox.config(state=tk.DISABLED)     

  if type_name in [TypeRole.DEBITO.value]:
    i_close_day.delete(0, tk.END)
    i_due_day.delete(0, tk.END)

    i_close_day.config(state=tk.DISABLED)
    i_due_day.config(state=tk.DISABLED)
    bank_combobox.config(state=tk.NORMAL)    

  if type_name in [TypeRole.CREDITO.value, TypeRole.CREDIARIO.value]:
    bank_combobox.delete(0, tk.END)

    i_close_day.config(state=tk.NORMAL)
    i_due_day.config(state=tk.NORMAL)
    bank_combobox.config(state=tk.DISABLED)    
  
def update_bank_combobox_fields(event=None):
  user_name = users_combobox.get()

  user_id = next((user.id for user in list_userss if user.name == user_name), None)

  list_banks = list_bank_accounts(user_id)

  banks = [bank.name for bank in list_banks]

  bank_combobox['values'] = (banks)

def button_create(frame):
  global add_img
  add_img = set_image('icons/icon-plus.png', 17, 17)

  global create_buttom
  create_buttom = tk.Button(frame, command=action_create, image=add_img, text='Adicionar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  create_buttom.place(x=20, y=200)

def action_create():
  user_name = users_combobox.get()
  description = i_description.get().strip()
  type_name = type_combobox.get()
  closed_day = int(i_close_day.get()) if i_close_day.get() not in [None, ''] else 0
  due_day = int(i_due_day.get()) if i_due_day.get() not in [None, ''] else 0
  bank_name = bank_combobox.get()

  if not user_name:
    messagebox.showwarning("Atenção", "O campo usuário não pode estar vazio.")
    return

  user_id = next((user.id for user in list_userss if user.name == user_name), None)

  if not user_id:
    messagebox.showwarning("Atenção", "Usuário não percente a lista")
    return

  if not description:
    messagebox.showwarning("Atenção", "O campo description não pode estar vazio.")
    return

  if not type_name:
    messagebox.showwarning("Atenção", "O campo Tipo não pode estar vazio.")
    return
  
  if type_name not in [TypeRole.DINHEIRO.value, TypeRole.DEBITO.value, TypeRole.CREDITO.value, TypeRole.CREDIARIO.value]:
    messagebox.showwarning("Atenção", "O tipo não percente a lista.")
    return

  if type_name in [TypeRole.CREDITO.value, TypeRole.CREDIARIO.value]:
    if not closed_day:
      messagebox.showwarning("Atenção", "O dia de fechamento não pode estar vazio.")
      return

    if not due_day:
      messagebox.showwarning("Atenção", "O dia de vencimento não pode estar vazio.")
      return
  
  bank_id = None

  if type_name in [TypeRole.DEBITO.value]:
    if not bank_name:
      messagebox.showwarning("Atenção", "O campo Banco não pode estar vazio.")
      return
    
    bank_id = next((bank.id for bank in list_bank_accounts(user_id) if bank.name == bank_name), None)

    if not user_id:
      messagebox.showwarning("Atenção", "Banco não percente a lista")
      return

  try:
    new_payment = create_payment(description, type_name, user_id, bank_id, due_day, closed_day)
    print(f"Instituição '{bank_name}' criada com sucesso.")
  except Exception as e:
    print(f"Erro ao criar a categoria: {e}")
    return

  users_combobox.delete(0, tk.END)
  i_description.delete(0, tk.END)
  type_combobox.delete(0, tk.END)
  i_close_day.delete(0, tk.END)
  i_due_day.delete(0, tk.END)
  bank_combobox.delete(0, tk.END)

  item = (
    new_payment.id,                     
    new_payment.name,
    new_payment.type,
    f"Dia {new_payment.closed_day}" if new_payment.closed_day else "",
    f"Dia {new_payment.due_day}" if new_payment.due_day else "",        
    bank_name if bank_name else "",
    user_name
  )

  add_item_table(item)

# >>>>>>>>>>>
# EDIT ACTION
# >>>>>>>>>>>

def button_edit(frame):
  global edit_img
  edit_img = set_image('icons/icon-edit.png', 17, 17)

  global edit_button
  edit_button = tk.Button(frame, command=action_edit, image=edit_img, text='Editar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  edit_button.place(x=130, y=200)

def action_edit():
  global current_selected_item

  selected_item = tree.selection()
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione um tipo de pagamento antes de editar.")
    return

  current_selected_item = selected_item[0]

  values = tree.item(current_selected_item, 'values')
  if values:
    i_description.delete(0, tk.END)
    i_description.insert(0, values[1])

    if values[2] in [TypeRole.CREDITO.value, TypeRole.CREDIARIO.value]:
      i_close_day.config(state=tk.NORMAL)
      i_due_day.config(state=tk.NORMAL)

      i_close_day.delete(0, tk.END)
      i_close_day.insert(0, int(values[3].split()[1]))

      i_due_day.delete(0, tk.END)
      i_due_day.insert(0, int(values[4].split()[1]))

     
    else:
      i_close_day.config(state=tk.DISABLED)
      i_due_day.config(state=tk.DISABLED)
  
  users_combobox.config(state=tk.DISABLED)
  type_combobox.config(state=tk.DISABLED)  
  bank_combobox.config(state=tk.DISABLED)

  create_buttom.config(state=tk.DISABLED)
  destroy_button.config(state=tk.DISABLED)

  edit_button.config(text='Salvar'.upper(), command=action_update)

def action_update():
  global current_selected_item

  new_description = i_description.get().strip()
  new_closed_day = int(i_close_day.get()) if i_close_day.get() not in [None, ''] else 0
  new_due_day = int(i_due_day.get()) if i_due_day.get() not in [None, ''] else 0

  if not new_description:
    messagebox.showwarning("Atenção", "A descrição do tipo de pagamento não pode estar vazio.")
    return

  line = tree.item(current_selected_item, 'values')

  payment_id = line[0]

  update_payment(payment_id, new_description, new_closed_day, new_due_day)

  new_closed_day = f"Dia {new_closed_day}" if new_closed_day else ""
  new_due_day = f"Dia {new_due_day}" if new_due_day else ""

  tree.item(current_selected_item, values=(payment_id, new_description, line[2], new_closed_day, new_due_day, line[5], line[6]))

  i_description.delete(0, tk.END)
  i_close_day.delete(0, tk.END)
  i_due_day.delete(0, tk.END)

  reset_edit_mode()

def reset_edit_mode():
  values = tree.item(current_selected_item, 'values')
  if values:
    i_description.delete(0, tk.END)
    i_close_day.delete(0, tk.END)
    i_due_day.delete(0, tk.END)

  edit_button.config(text='Editar'.upper(), command=action_edit)
  
  users_combobox.config(state=tk.NORMAL)
  type_combobox.config(state=tk.NORMAL)

  i_close_day.config(state=tk.DISABLED)
  i_due_day.config(state=tk.DISABLED)

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
  destroy_button.place(x=240, y=200)

def destroy():
  selected_item = tree.selection()  
  
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione um tipo de pagamento.")
    return

  payment_id = int(tree.item(selected_item, 'values')[0])  

  if transaction_exists([payment_id]):
    messagebox.showwarning("Atenção", "Tipo de pagamento possui transações")
    return

  delete_payment(payment_id)

  tree.delete(selected_item)

def transaction_exists(payment_ids):
  objects = list_transactions_values_expenses_to_categories(None, None, None, None, payment_ids)
  return True if len(objects) > 0 else False
