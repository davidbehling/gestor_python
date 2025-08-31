import tkinter as tk
import tkinter.messagebox as messagebox 
from tkinter import ttk

from ..colors import *
from ..header import header

from global_values import *

from repository.category_repository import list_categories, create_category, update_category, delete_category
from repository.transaction_repository import list_transactions_values_expenses_to_categories

from services.tools import set_image

current_selected_item = None

def categories_init(main_frame, args=None):
  header(main_frame, 'Categorias', 'icons/icon-categories.png')

  frame_body = tk.Frame(main_frame, width=body_width, height=body_height, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=footer_width, height=footer_height, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  tab(frame_body)
  radio_select(frame_body)

  input_radio(frame_footer)
  input_name(frame_footer)
  button_create(frame_footer)
  button_edit(frame_footer)
  button_destroy(frame_footer)

# >>>>>>>>>>>>>
# TABELA ACTION
# >>>>>>>>>>>>>

def tab(frame, expense=None):
  tab_head = ['#Id', 'Categoria', 'Tipo']

  global tree

  tree = ttk.Treeview(frame, selectmode="extended",columns=tab_head, show="headings")

  vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
  
  hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

  tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

  # Adicionando a Treeview e as Scrollbars ao layout com margens
  tree.grid(column=0, row=0, sticky='nsew', padx=(150, 5), pady=5)    # Margens internas
  vsb.grid(column=1, row=0, sticky='ns', padx=(0, 5), pady=5)  # Margem direita
  #hsb.grid(column=0, row=1, sticky='ew', padx=150, pady=(0, 5))  # Margem inferior

  hd=["center","w","center"]
  h=[30,400,100]
  n=0

  for col in tab_head:
    tree.heading(col, text=col.title(), anchor=tk.CENTER)      
    tree.column(col, width=h[n],anchor=hd[n])    
    n+=1
  
  tree.tag_configure("last_col_red", foreground="red", font=('Arial', 10, 'bold'))
  tree.tag_configure("last_col_green", foreground="green", font=('Arial', 10, 'bold'))

  seed_table(expense)

  # Configurando o evento no Treeview
  tree.bind("<<TreeviewSelect>>", on_tree_select)

def seed_table(expense):
  categories = list_categories(expense)

  lista_itens = [
    (
        category.id,                     
        category.name,                    
        'Despesa' if category.expense else 'Receita'
    )
    for category in categories
  ]

  for item in lista_itens:
    add_item_table(item)

def add_item_table(item):
  item_id = tree.insert('', 'end', values=item)

  tipo = item[2]

  if tipo == 'Despesa':
    tree.item(item_id, tags=("last_col_red",))
  else:
    tree.item(item_id, tags=("last_col_green",))

def refresh_table(expense=None):
    for item in tree.get_children():
      tree.delete(item)

    seed_table(expense)

# >>>>>>>>>>>>>>>>>>>>
# FILTRO DE CATEGORIAS
# >>>>>>>>>>>>>>>>>>>>

def radio_select(frame):
  radio_select_var = tk.IntVar(value=1)

  coo_x = 750

  l_type = tk.Label(frame, text='Filtro por Tipo', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_type.place(x=coo_x, y=20)  

  tk.Radiobutton(frame, text="Todos", variable=radio_select_var, value=1, command=lambda: refresh_table(None)).place(x=coo_x, y=50)
  tk.Radiobutton(frame, text="Despesa", variable=radio_select_var, value=2, command=lambda: refresh_table(True)).place(x=coo_x, y=80)
  tk.Radiobutton(frame, text="Receita", variable=radio_select_var, value=3, command=lambda: refresh_table(False)).place(x=coo_x, y=110)

# >>>>>>>>>>>>>
# CREATE ACTION
# >>>>>>>>>>>>>

def input_radio(frame):
  global radio_var
  radio_var = tk.BooleanVar(value=True)

  l_name = tk.Label(frame, text='Tipo', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_name.place(x=20, y=20)

  tk.Radiobutton(frame, text="Despesa", variable=radio_var, value=True).place(x=120, y=20)
  tk.Radiobutton(frame, text="Receita", variable=radio_var, value=False).place(x=220, y=20)

def input_name(frame):
  global i_name

  l_name = tk.Label(frame, text='Nome', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_name.place(x=20, y=60)

  i_name = tk.Entry(frame, width=12, justify=tk.LEFT, relief=tk.SOLID)
  i_name.place(x=120, y=60)

def button_create(frame):
  global add_img
  add_img = set_image('icons/icon-plus.png', 17, 17)

  global create_buttom
  create_buttom = tk.Button(frame, command=action_create, image=add_img, text='Adicionar'.upper(), width=75, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  create_buttom.place(x=20, y=110)

def action_create():
  category_name = i_name.get().strip()
  is_expense = radio_var.get()

  if not category_name:
    messagebox.showwarning("Atenção", "O nome da categoria não pode estar vazio.")
    return
  
  if is_expense == None:
    messagebox.showwarning("Atenção", "Marcar um tipo de categoria: Despesas ou Receita.")
    return
  
  try:
    new_category = create_category(category_name, is_expense)
    print(f"Categoria '{category_name}' criada com sucesso.")
  except Exception as e:
    print(f"Erro ao criar a categoria: {e}")
    return

  i_name.delete(0, tk.END)

  item = (new_category.id, new_category.name, 'Despesa' if new_category.expense else 'Receita')

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

def action_edit():
  global current_selected_item

  selected_item = tree.selection()
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione uma categoria antes de editar.")
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

  category_id = tree.item(current_selected_item, 'values')[0]

  update_category(category_id, new_name)

  tree.item(current_selected_item, values=(category_id, new_name, "Despesa"))  # Ajuste conforme necessário

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
  destroy_button.place(x=240, y=110)

def destroy():
  selected_item = tree.selection()  
  
  if not selected_item:
    messagebox.showwarning("Atenção", "Selecione uma categoriar.")
    return

  id = tree.item(selected_item, 'values')[0]

  if transaction_exists(id):
    messagebox.showwarning("Atenção", "Categoria esta sendo utilizada em transações.")
    return

  delete_category(id)

  tree.delete(selected_item)

def transaction_exists(id):
  objects = list_transactions_values_expenses_to_categories(None, None, None, [id])
  return True if len(objects) > 0 else False
