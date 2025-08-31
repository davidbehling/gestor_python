import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from calendar import monthrange
from datetime import datetime, date

from components.mult_select_obj_v2 import MultiSelectCombobox

from repository.category_repository import list_categories
from repository.user_repository import list_users

from services.tools import set_image, retroactive_date, postponed_date

from ..colors import *

def search_criteria(frame, main_frame, inicial_date_start, inicial_date_end, inicial_user_ids, inicial_category_ids):
  input_date_start(frame, inicial_date_start)
  input_date_end(frame, inicial_date_end)
  input_users(frame, inicial_user_ids)
  input_categories(frame, inicial_category_ids)
  button_search(frame, main_frame)
  left_arrow(frame, main_frame)
  right_arrow(frame, main_frame)

def input_date_start(frame, inicial_date_start):
  global date_start

  l_date = tk.Label(frame, text='Data inicial', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_date.place(x=550, y=10)

  date_start = DateEntry(frame, width=11, background='darkblue', foreground='white', borderwidth=2)
  date_start.place(x=650, y=10)

  date_start.set_date(inicial_date_start)

def input_date_end(frame, inicial_date_end):
  global date_end

  l_date = tk.Label(frame, text='Data final', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_date.place(x=550, y=40)

  date_end = DateEntry(frame, width=11, background='darkblue', foreground='white', borderwidth=2)
  date_end.place(x=650, y=40)

  date_end.set_date(inicial_date_end)


def input_users(frame, inicial_values=None):
  global users_combobox

  l_users = tk.Label(frame, text='Usuários', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_users.place(x=550, y=70)

  users = list_users()

  users_combobox = MultiSelectCombobox(frame, objects=users, display_property="name", value_property="id", initial_values=inicial_values, width=11)
  users_combobox.place(x=650, y=70)

def input_categories(frame, inicial_values=None):
  global categories_combobox

  l_category = tk.Label(frame, text='Categorias', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_category.place(x=550, y=100)

  categories = list_categories(True)

  categories_combobox = MultiSelectCombobox(frame, objects=categories, display_property="name", value_property="id", initial_values=inicial_values, width=11)
  categories_combobox.place(x=650, y=100)

def button_search(frame, main_frame):
  global trash_img
  trash_img = set_image('icons/icon-search.png', 17, 17)

  buttom = tk.Button(frame, command=lambda c=main_frame: seach_action(c), image=trash_img, text='Busca'.upper(), width=70, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=550, y=130)

def seach_action(main_frame):
  date_start_at = datetime.strptime(date_start.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
  data_end_at = datetime.strptime(date_end.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
  users = users_combobox.get_selected_values()
  categories = categories_combobox.get_selected_values()

  args = { 
    'date_start': date_start_at,
    'date_end': data_end_at,
    'user_ids': users,
    'category_ids': categories
  }

  from .dashboard import dashboard_init
  dashboard_init(main_frame, args)

def left_arrow(frame, main_frame):
  global left_arrow_img
  left_arrow_img = set_image('icons/icon-left-arrow.png', 17, 17)

  buttom = tk.Button(frame, command=lambda c=main_frame: left_action(c), image=left_arrow_img, width=17  , compound=tk.LEFT, anchor=tk.NW, bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=690, y=130)

def left_action(main_frame):
  dates = retroactive_date(date_start.get())
  date_start.set_date(dates['first_date'])
  date_end.set_date(dates['last_date'])
  seach_action(main_frame)

def right_arrow(frame, main_frame):
  global right_arrow_img
  right_arrow_img = set_image('icons/icon-right-arrow.png', 17, 17)

  buttom = tk.Button(frame, command=lambda c=main_frame: right_action(c), image=right_arrow_img, width=17  , compound=tk.LEFT, anchor=tk.NW, bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=720, y=130)

def right_action(main_frame):
  dates = postponed_date(date_start.get())
  date_start.set_date(dates['first_date'])
  date_end.set_date(dates['last_date'])
  seach_action(main_frame)
