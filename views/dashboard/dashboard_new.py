import random
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Progressbar
from tkcalendar import DateEntry
from calendar import monthrange
from datetime import datetime, date

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from global_values import *

from ..colors import *
from ..header import header

from services.tools import set_image, first_day_of_current_month, last_day_of_current_month, date_string_to_datatime, retroactive_date, postponed_date
from services.dashboard_service import calculation_percent

from repository.category_repository import list_categories
from repository.transaction_repository import list_transactions_values_expenses_to_categories, total_expenses_and_incomes_values
from repository.user_repository import list_users

from components.mult_select_obj_v2 import MultiSelectCombobox
from components.bar_and_pie_chart import BarAndPieChart

canvas = None
ax = None

categories_canvas = None
categories_ax = None

chart = None

summary_values = []
legend_labels = []

def dashboard_init_new(main_frame, args=None):
  header(main_frame, 'Dashboard', 'icons/icon-dashboard.png')

  frame_body = tk.Frame(main_frame, width=body_width, height=body_height, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=footer_width, height=footer_height, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  percent_progress_bar(frame_body)

  income_and_expense_chart(frame_body)

  income_and_expense_summary(frame_body)

  search_criteria(frame_body)

  expense_pie_chart(frame_footer, [])

  generete_values(first_day_of_current_month(), last_day_of_current_month(), None, None)

def generete_values(date_start, date_end, user_ids, category_ids):
  data = total_expenses_and_incomes_values(date_start, date_end, user_ids, category_ids)

  value_expense = ([item['value'] for item in data if item['expense']])[0]

  value_income = ([item['value'] for item in data if not item['expense']])[0]

  percent_progress_bar_reload(value_income, value_expense)

  income_and_expense_chart_reload(value_income, value_expense)

  income_and_expense_summary_reload(value_income, value_expense)

  list_transactions = list_transactions_values_expenses_to_categories(date_start, date_end, user_ids, category_ids)

  global chart

  chart.update_chart(list_transactions)

# ============================
# Gráfico - Barra de Progresso
# ============================

def percent_progress_bar(frame):
  # Título.
  label_name = tk.Label(frame, text='Porcentagem da receita gasta', height=1, anchor=tk.NW, font=('Verdana 12'), bg=co1, fg=co4)
  label_name.place(x=7, y=5)

  # Barra de Progresso.
  styles = ttk.Style()
  styles.theme_use('default')
  styles.configure('black.Horizontal.TProgressbar', background='#daed6b')
  styles.configure('TProgressbar', thickness=25)

  global progressbar
  progressbar = Progressbar(frame, length=180, style='black.Horizontal.TProgressbar')
  progressbar.place(x=10, y=35)
  progressbar['value'] = 0

  # Valor percentual exibido ao lado da barra de progresso.
  global label_percent
  label_percent = tk.Label(frame, text="{:,.2f}%".format(0), anchor=tk.NW, font=('Verdana 12'), bg=co1, fg=co4)
  label_percent.place(x=200, y=35)

def percent_progress_bar_reload(income, expense):
  value_percent = calculation_percent(income, expense)

  progressbar['value'] = value_percent

  label_percent.config(text="{:,.2f}%".format(value_percent))

# ===========================
# Gráfico - Colunas de Barras
# ===========================

def income_and_expense_chart(frame):
  global canvas, ax

  values = [0, 0, 0] 

  figura = plt.Figure(figsize=(4, 3.45), dpi=60)

  ax = figura.add_subplot(111)
  
  configure_draw(values)

  canvas = FigureCanvasTkAgg(figura, frame)

  canvas.get_tk_widget().place(x=10, y=70)

def income_and_expense_chart_reload(income, expense):
  global canvas, ax

  values = [income, expense, (income - expense)]

  ax.clear()

  configure_draw(values)

  canvas.draw()
  
def configure_draw(values):
  global ax

  categories = ['Renda', 'Despesas', 'Saldo']

  ax.bar(categories, values, color=colors, width=0.9)

  c = 0
  for i in ax.patches:
      ax.text(i.get_x() - .001, i.get_height() + .5,
              str("{:,.0f}".format(values[c])), fontsize=17, fontstyle='italic', 
              verticalalignment='bottom', color='dimgrey')
      c += 1

  ax.set_xticklabels(categories, fontsize=16)
  ax.patch.set_facecolor('#ffffff')
  ax.spines['bottom'].set_color('#CCCCCC')
  ax.spines['bottom'].set_linewidth(1)
  ax.spines['right'].set_linewidth(0)
  ax.spines['top'].set_linewidth(0)
  ax.spines['left'].set_color('#CCCCCC')
  ax.spines['left'].set_linewidth(1)
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(False)
  ax.tick_params(bottom=False, left=False)
  ax.set_axisbelow(True)
  ax.yaxis.grid(False, color='#EEEEEE')
  ax.xaxis.grid(False)

# =================
# Resumo financeiro
# =================

def income_and_expense_summary(frame):
  global summary_values

  summary_values.clear()

  categories = ['Total da Renda               ', 
                'Total de Despesas            ', 
                'Total de Saldo               ']

  values = [0, 0, 0]

  place_y = [[52, 35, 70], [132, 115, 150], [207, 190, 220]]

  for i in range(0, 3):
    l_line = tk.Label(frame, text='', width=215, height=1, anchor=tk.NW, font=('Arial 1'), bg='#545454')
    l_line.place(x=309, y=place_y[i][0])

    l_summary = tk.Label(frame, text=categories[i].upper(), anchor=tk.NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_summary.place(x=309, y=place_y[i][1])

    l_value = tk.Label(frame, text="R$ {:,.2f}".format(values[i]), anchor=tk.NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_value.place(x=309, y=place_y[i][2])

    summary_values.append(l_value)

def income_and_expense_summary_reload(income, expense):
  global summary_values

  values = [income, expense, (income - expense)]

  for i in range(len(summary_values)):
    summary_values[i].config(text="R$ {:,.2f}".format(values[i]))  

# =============
# LUPA - SEATCH
# =============

def search_criteria(frame):
  input_date_start(frame)
  input_date_end(frame)
  input_users(frame)
  input_categories(frame)
  button_search(frame)
  left_arrow(frame)
  right_arrow(frame)

def input_date_start(frame):
  global date_start

  l_date = tk.Label(frame, text='Data inicial', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_date.place(x=550, y=10)

  date_start = DateEntry(frame, width=11, background='darkblue', foreground='white', borderwidth=2)
  date_start.place(x=650, y=10)

  date_start.set_date(first_day_of_current_month())

def input_date_end(frame):
  global date_end

  l_date = tk.Label(frame, text='Data final', height=1, anchor=tk.NW, font=('Ivy 10'), bg=co1, fg=co4)
  l_date.place(x=550, y=40)

  date_end = DateEntry(frame, width=11, background='darkblue', foreground='white', borderwidth=2)
  date_end.place(x=650, y=40)

  date_end.set_date(last_day_of_current_month())


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

def button_search(frame):
  global trash_img
  trash_img = set_image('icons/icon-search.png', 17, 17)

  buttom = tk.Button(frame, command=seach_action, image=trash_img, text='Busca'.upper(), width=70, compound=tk.LEFT, anchor=tk.NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=550, y=130)

def seach_action():
  date_start_at = datetime.strptime(date_start.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
  data_end_at = datetime.strptime(date_end.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
  users = users_combobox.get_selected_values()
  categories = categories_combobox.get_selected_values()

  generete_values(date_start_at, data_end_at, users, categories)

def left_arrow(frame):
  global left_arrow_img
  left_arrow_img = set_image('icons/icon-left-arrow.png', 17, 17)

  buttom = tk.Button(frame, command=left_action, image=left_arrow_img, width=17  , compound=tk.LEFT, anchor=tk.NW, bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=690, y=130)

def left_action():
  dates = retroactive_date(date_start.get())
  date_start.set_date(dates['first_date'])
  date_end.set_date(dates['last_date'])
  seach_action()

def right_arrow(frame):
  global right_arrow_img
  right_arrow_img = set_image('icons/icon-right-arrow.png', 17, 17)

  buttom = tk.Button(frame, command=right_action, image=right_arrow_img, width=17  , compound=tk.LEFT, anchor=tk.NW, bg=co1, fg=co0, overrelief=tk.RIDGE)
  buttom.place(x=720, y=130)

def right_action():
  dates = postponed_date(date_start.get())
  date_start.set_date(dates['first_date'])
  date_end.set_date(dates['last_date'])
  seach_action()

# =========
# PIE CHART
# =========

def expense_pie_chart(frame_footer, list_transactions):
  global chart
  chart = BarAndPieChart(frame_footer, list_transactions)

