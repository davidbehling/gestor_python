import tkinter as tk
import tkinter.messagebox as messagebox 
from tkcalendar import DateEntry
from tkinter import ttk

from datetime import datetime

from decimal import Decimal

from components.mult_select_obj_v2 import MultiSelectCombobox

from ..colors import *
from ..header import header

from global_values import *

from models.payment import TypeRole
from models.transaction import Transaction

from repository.category_repository import list_categories
from repository.payment_repository import list_payments_by_user_id
from repository.transaction_repository import list_transactions_details, update_transaction, find_transaction_id, delete_transaction, confirm_pay
from repository.user_repository import list_users

from services.transaction_service import create_transaction_serv
from services.tools import set_image, data_datatime_to_string, to_money, to_string_date_br, is_decimal, date_string_to_datatime, real_coin_to_decimal, first_day_of_current_month, last_day_of_current_month, retroactive_date, postponed_date

current_selected_item = None

def incomes_init(main_frame, args=None):
  header(main_frame, 'Receitas', 'icons/icon-income.png')

  frame_body = tk.Frame(main_frame, width=body_width, height=body_height, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=footer_width, height=footer_height, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  tab(frame_body)

  crud_transaction(frame_footer)

  filter(frame_footer)



# >>>>>>>>>>>>>
# TABELA ACTION
# >>>>>>>>>>>>>

def tab(frame):
  #tab_head = ['#Id', 'Vencimento', 'Categoria', 'Descrição', 'Valor', 'Pagamento','Pago', 'Parcela', 'Data Compra','Usuário']

  tab_config = [
    {'col': '#Id', 'hd': 'center', 'h': 30},
    {'col': 'Data', 'hd': 'w', 'h': 95},
    {'col': 'Categoria', 'hd': 'w', 'h': 100},
    {'col': 'Descrição', 'hd': 'w', 'h': 110},
    {'col': 'Valor', 'hd': 'w', 'h': 100},
    {'col': 'Pagamento', 'hd': 'w', 'h': 100},  
    {'col': 'Usuário', 'hd': 'w', 'h': 100},
  ]

  tab_head = [item['col'] for item in tab_config]

  global tree

  tree = ttk.Treeview(frame, selectmode="extended",columns=tab_head, show="headings")

  vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
  
  hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

  tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

  # Adicionando a Treeview e as Scrollbars ao layout com margens
  tree.grid(column=0, row=0, sticky='nsew', padx=(5, 5), pady=5)    # Margens internas
  vsb.grid(column=1, row=0, sticky='ns', padx=(0, 5), pady=5)  # Margem direita

  hd = [item['hd'] for item in tab_config]
  h = [item['h'] for item in tab_config]
  n=0

  for col in tab_head:
    tree.heading(col, text=col.title(), anchor=tk.CENTER)      
    tree.column(col, width=h[n],anchor=hd[n])    
    n+=1
  
  seed_table(defaut_seed_args())

  tree.bind("<<TreeviewSelect>>", on_tree_select)

def defaut_seed_args():
  args = {}
  args['expense'] = False
  args['date_start'] = first_day_of_current_month()
  args['date_end'] = last_day_of_current_month()
  args['user_ids'] = None
  args['category_ids'] = None
  args['payment_ids'] = None
  args['paid'] = None
  return args

def seed_table(args):
  for item in tree.get_children():
      tree.delete(item)

  transactions = list_transactions_details(args['expense'], args['date_start'], args['date_end'], args['user_ids'], args['category_ids'], args['payment_ids'], args['paid'])

  lista_itens = [
    (
        transaction.id,                     
        to_string_date_br(transaction.date_at),
        transaction.category_name,
        transaction.description,
        to_money(transaction.value),
        transaction.payment_name,        
        transaction.user_name
    )
    for transaction in transactions
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
      reset_fields()

# >>>>>>>>>>>
# CRUD ACTION
# >>>>>>>>>>>

def crud_transaction(frame_footer):
  input_date_at(frame_footer)
  input_user(frame_footer)  
  input_category(frame_footer)
  input_payment(frame_footer)
  input_description(frame_footer)
  input_value(frame_footer)

  button_create(frame_footer)

  button_edit(frame_footer)

  button_destroy(frame_footer)

  update_payment_combobox_fields()

# >>>>>>>>>>>>>
# CREATE ACTION
# >>>>>>>>>>>>>

def input_date_at(frame):
  global i_date_at

  l_date = tk.Label(frame, text='Data inicial', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_date.place(x=20, y=20)

  i_date_at = DateEntry(frame, width=11, background='darkblue', foreground='white', borderwidth=2)
  i_date_at.place(x=170, y=20)

def input_user(frame):
  global users_combobox

  l_user = tk.Label(frame, text='Usuário', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_user.place(x=20, y=50)

  global list_userss
  list_userss = list_users()

  users = [user.name for user in list_userss]

  users_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  users_combobox['values'] = (users)
  users_combobox.place(x=170, y=50)

  users_combobox.bind("<<ComboboxSelected>>", update_payment_combobox_fields)

def update_payment_combobox_fields(event=None):
  user_name = users_combobox.get()

  user_id = next((user.id for user in list_userss if user.name == user_name), None)

  global list_payments
  list_payments = list_payments_by_user_id(user_id)

  payments = [payment.name for payment in list_payments if payment.type in [TypeRole.DINHEIRO.value, TypeRole.DEBITO.value]]

  payments_combobox['values'] = (payments)

def input_category(frame):
  global categories_combobox

  l_type = tk.Label(frame, text='Receita', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_type.place(x=20, y=80)

  global list_categoriess
  list_categoriess = list_categories(False)

  categories = [category.name for category in list_categoriess]

  categories_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  categories_combobox['values'] = (categories)
  categories_combobox.place(x=170, y=80)

def input_payment(frame):
  global payments_combobox

  l_type = tk.Label(frame, text='Depósito em', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_type.place(x=20, y=110)

  payments_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  payments_combobox['values'] = ([])
  payments_combobox.place(x=170, y=110)

def input_description(frame):
  global i_description

  l_description = tk.Label(frame, text='Descrição', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_description.place(x=20, y=140)

  i_description = tk.Entry(frame, width=12, justify=tk.LEFT, relief=tk.SOLID)
  i_description.place(x=170, y=140)

def input_value(frame):
  global i_value

  l_value = tk.Label(frame, text='Valor', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_value.place(x=20, y=170)

  vcmd = (frame.register(is_decimal), "%P")

  i_value = tk.Entry(frame, width=12, justify=tk.LEFT, relief=tk.SOLID,  validate="key", validatecommand=vcmd)
  i_value.place(x=170, y=170)

def button_create(frame):
  global add_img
  add_img = set_image('icons/icon-plus.png', 17, 17)

  global create_buttom
  create_buttom = tk.Button(frame, command=action_create, image=add_img, text='Adicionar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  create_buttom.place(x=20, y=200)

def action_create():
  validateFields()

  date_at = datetime.strptime(i_date_at.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
  user_name = users_combobox.get()
  category_name = categories_combobox.get()
  payment_name = payments_combobox.get()
  description = i_description.get().strip()
  value = float(Decimal(i_value.get())) if i_value.get() not in [None, ''] else None

  user_id = next((user.id for user in list_userss if user.name == user_name), None)

  category_id = next((category.id for category in list_categoriess if category.name == category_name), None)

  payment = next((payment for payment in list_payments if payment.name == payment_name), None)

  objects = create_transaction_serv(description, value, date_at, user_id, category_id, payment.id, None)

  reset_fields()

  new_transactions = [objects] if isinstance(objects, Transaction) > 0 else objects

  for new_transaction in new_transactions:
    item = (
      new_transaction.id,                     
      to_string_date_br(new_transaction.payment_date),
      category_name,
      new_transaction.description,
      to_money(new_transaction.value),
      payment_name,     
      user_name
    )

    add_item_table(item)

def validateFields():
  date_at = datetime.strptime(i_date_at.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
  user_name = users_combobox.get()
  category_name = categories_combobox.get()
  payment_name = payments_combobox.get()
  description = i_description.get().strip()
  value = float(Decimal(i_value.get())) if i_value.get() not in [None, ''] else None

  if not date_at:
    messagebox.showwarning("Atenção", "O campo Data não pode estar vazio.")
    return
  
  if not user_name:
    messagebox.showwarning("Atenção", "O campo Usuário não pode estar vazio.")
    return

  user_id = next((user.id for user in list_userss if user.name == user_name), None)

  if not user_id:
    messagebox.showwarning("Atenção", "Usuário não percente a lista")
    return
  
  if not category_name:
    messagebox.showwarning("Atenção", "O campo Receita não pode estar vazio.")
    return
  
  category_id = next((category.id for category in list_categoriess if category.name == category_name), None)

  if not category_id:
    messagebox.showwarning("Atenção", "Receita não percente a lista")
    return
  
  if not payment_name:
    messagebox.showwarning("Atenção", "O campo tipo de deposito não pode estar vazio.")
    return
    
  payment = next((payment for payment in list_payments if payment.name == payment_name), None)

  if not payment:
    messagebox.showwarning("Atenção", "Tipo de depóstio não percente a lista")
    return

  if not description:
    messagebox.showwarning("Atenção", "O campo Descrição não pode estar vazio.")
    return

  if not value:
    messagebox.showwarning("Atenção", "O campo Valor não pode estar vazio.")
    return

def reset_fields():
  i_date_at.delete(0, 'end')
  users_combobox.delete(0, 'end')
  categories_combobox.delete(0, 'end')
  payments_combobox.delete(0, 'end')
  i_description.delete(0, 'end')
  i_value.delete(0, 'end')

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
    messagebox.showwarning("Atenção", "Selecione uma receita antes de editar.")
    return

  current_selected_item = selected_item[0]

  result = current_select_line()

  if result:
    reset_fields()
    set_fields(result)
  
  create_buttom.config(state=tk.DISABLED)
  destroy_button.config(state=tk.DISABLED)

  edit_button.config(text='Salvar'.upper(), command=action_update)

def current_select_line():
  result = dict(zip(tree["columns"], tree.item(current_selected_item, 'values')))
  result['#Id'] = int(result['#Id'])
  result['Valor'] = real_coin_to_decimal(result['Valor'])
  return result

def set_fields(result):
    i_date_at.set_date(datetime.strptime(result['Data'], '%d/%m/%Y'))
    users_combobox.set(result['Usuário'])
    update_payment_combobox_fields()
    categories_combobox.set(result['Categoria'])
    payments_combobox.set(result['Pagamento'])
    i_description.insert(0, result['Descrição'])
    i_value.insert(0, result['Valor'])

def action_update():
  global current_selected_item

  validateFields()

  date_at = datetime.strptime(i_date_at.get(), '%d/%m/%Y') #.strftime('%Y-%m-%d')
  user_name = users_combobox.get()
  category_name = categories_combobox.get()
  payment_name = payments_combobox.get()
  description = i_description.get().strip()
  value = float(Decimal(i_value.get())) if i_value.get() not in [None, ''] else None

  user_id = next((user.id for user in list_userss if user.name == user_name), None)

  category_id = next((category.id for category in list_categoriess if category.name == category_name), None)

  payment = next((payment for payment in list_payments if payment.name == payment_name), None)

  line = tree.item(current_selected_item, 'values')

  transaction_id = line[0]

  update_transaction(transaction_id, description, value, date_at, user_id, category_id, payment.id, None)

  new_transaction = find_transaction_id(transaction_id)

  item = (
    new_transaction.id,                     
    to_string_date_br(new_transaction.date_at),
    category_name,
    new_transaction.description,
    to_money(new_transaction.value),
    payment_name,
    user_name
  )

  tree.item(current_selected_item, values=item)

  reset_edit_mode()

  reset_fields()

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
  destroy_button.place(x=240, y=200)

def destroy():
  selected_item = tree.selection()  
  
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione uma receita.")
    return

  id = int(tree.item(selected_item, 'values')[0])  

  delete_transaction(id)

  tree.delete(selected_item)

# >>>>>>>>>>>>>
# FITLER ACTION
# >>>>>>>>>>>>>

def filter(frame_footer):
  l_type = tk.Label(frame_footer, text='Filtro:', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_type.place(x=600, y=10)

  left_arrow(frame_footer)
  right_arrow(frame_footer)

  input_date_start_filter(frame_footer)
  input_date_end_filter(frame_footer)
  input_users_filter(frame_footer)
  input_categories_filter(frame_footer)
  input_payments_filter(frame_footer)
  button_search(frame_footer)
  button_search_clear(frame_footer)

def input_date_start_filter(frame):
  global date_f_start

  l_f_date = tk.Label(frame, text='Data inicial.', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_f_date.place(x=600, y=40)

  date_f_start = DateEntry(frame, width=11, background='darkblue', foreground='white', borderwidth=2)
  date_f_start.place(x=750, y=40)

  date_f_start.set_date(first_day_of_current_month())

def input_date_end_filter(frame):
  global date_f_end

  l_f_date = tk.Label(frame, text='Data final.', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_f_date.place(x=600, y=70)

  date_f_end = DateEntry(frame, width=11, background='darkblue', foreground='white', borderwidth=2)
  date_f_end.place(x=750, y=70)

  date_f_end.set_date(last_day_of_current_month())

def input_users_filter(frame):
  global users_f_combobox

  l_f_users = tk.Label(frame, text='Usuários', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_f_users.place(x=600, y=100)

  global list_f_userss
  list_f_userss = list_users()

  users = [user.name for user in list_f_userss]

  users_f_combobox = ttk.Combobox(frame, width=11, font=('Ivy 10'))
  users_f_combobox['values'] = (users)
  users_f_combobox.place(x=750, y=100)

  if len(users) > 0:
    users_f_combobox.set(users[0])

  users_f_combobox.bind("<<ComboboxSelected>>", update_payment_filters_combobox_fields)

def input_categories_filter(frame, inicial_values=None):
  global categories_f_combobox

  l_f_category = tk.Label(frame, text='Categorias', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_f_category.place(x=600, y=130)

  categories = list_categories(False)

  categories_f_combobox = MultiSelectCombobox(frame, objects=categories, display_property="name", value_property="id", initial_values=inicial_values, width=11)
  categories_f_combobox.place(x=750, y=130)

def input_payments_filter(frame, inicial_values=None):
  global payments_f_combobox
  global list_payments

  payments = []

  l_f_payment = tk.Label(frame, text='Pagamentos', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_f_payment.place(x=600, y=160)

  user_name = users_f_combobox.get()

  if user_name != None or user_name != "":
    user_id = next((user.id for user in list_f_userss if user.name == user_name), None)
    
    list_payments = list_payments_by_user_id(user_id)
    payments = [payment for payment in list_payments if payment.type in [TypeRole.DINHEIRO.value, TypeRole.DEBITO.value]]

  payments_f_combobox = MultiSelectCombobox(frame, objects=payments, display_property="name", value_property="id", initial_values=inicial_values, width=11)
  payments_f_combobox.place(x=750, y=160)

  update_payment_filters_combobox_fields

def update_payment_filters_combobox_fields(event=None):
  user_name = users_f_combobox.get()

  user_id = next((user.id for user in list_f_userss if user.name == user_name), None)

  global list_payments
  list_payments = list_payments_by_user_id(user_id)
  payments = [payment for payment in list_payments if payment.type in [TypeRole.DINHEIRO.value, TypeRole.DEBITO.value]]

  payments_f_combobox.reset_objects(payments, initial_values=None)

def button_search(frame):
  global search_img
  search_img = set_image('icons/icon-search.png', 17, 17)

  buttom = tk.Button(frame, command=seach_action, image=search_img, text='Busca'.upper(), width=70, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=600, y=190)

def seach_action():
  f_date_start = datetime.strptime(date_f_start.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
  f_date_end = datetime.strptime(date_f_end.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
  f_category_ids = categories_f_combobox.get_selected_values()
  f_payment_ids = payments_f_combobox.get_selected_values()
  
  user_name = users_f_combobox.get()

  f_user_id = next((user.id for user in list_f_userss if user.name == user_name), None)

  params = {
    'expense': False,
    'date_start': f_date_start,
    'date_end': f_date_end,
    'category_ids': f_category_ids,
    'payment_ids': f_payment_ids,
    'user_ids': [f_user_id],
    'paid': None
  }

  seed_table(params)

def button_search_clear(frame):
  global search_clear_img
  search_clear_img = set_image('icons/icon-filter-clear.png', 17, 17)

  buttom = tk.Button(frame, command=lambda c=defaut_seed_args(): seed_table(c), image=search_clear_img, text='Limpar'.upper(), width=70, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=705, y=190)

def left_arrow(frame):
  global left_arrow_img
  left_arrow_img = set_image('icons/icon-left-arrow.png', 17, 17)

  buttom = tk.Button(frame, command=left_action, image=left_arrow_img, width=17  , compound=tk.LEFT, anchor=tk.NW, bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=750, y=10)

def left_action():
  dates = retroactive_date(date_f_start.get())
  date_f_start.set_date(dates['first_date'])
  date_f_end.set_date(dates['last_date'])
  seach_action()

def right_arrow(frame):
  global right_arrow_img
  right_arrow_img = set_image('icons/icon-right-arrow.png', 17, 17)

  buttom = tk.Button(frame, command=right_action, image=right_arrow_img, width=17  , compound=tk.LEFT, anchor=tk.NW, bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=830, y=10)

def right_action():
  dates = postponed_date(date_f_start.get())
  date_f_start.set_date(dates['first_date'])
  date_f_end.set_date(dates['last_date'])
  seach_action()