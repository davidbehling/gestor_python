import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


from ..colors import *
from ..header import header

from .percent_progress import percent_progress_bar
from .columns_chart import income_and_expense_chart
from .summary_finances import income_and_expense_summary
from .pie_chart import expense_pie_chart
from .search import search_criteria

from services.tools import set_image, first_day_of_current_month, last_day_of_current_month, date_string_to_datatime
from services.dashboard_service import calculation_percent

from repository.transaction_repository import list_transactions_values_expenses_to_categories, total_expenses_and_incomes_values

def dashboard_init(main_frame, args=None):
  header(main_frame, 'Dashboard', 'icons/icon-dashboard.png')

  frame_body = tk.Frame(main_frame, width=1043, height=361, bg=co1, pady=20, relief='raised')
  frame_body.grid(row=1, column=0, pady=1, padx=0, sticky=tk.NSEW)

  frame_footer = tk.Frame(main_frame, width=1043, height=300, bg="white", relief='raised')
  frame_footer.grid(row=2, column=0, pady=0, padx=0, sticky=tk.NSEW)

  inicial_date_start = first_day_of_current_month()
  inicial_date_end = last_day_of_current_month()
  inicial_user_ids = None
  inicial_category_ids = None
  
  date_start = inicial_date_start
  date_end = inicial_date_end
  user_ids = None
  category_ids = None

  params = args

  if params != None:
    if 'user_ids' in params and len(params['user_ids']) > 0: 
      user_ids = params['user_ids']
      inicial_user_ids = user_ids
    if 'category_ids' in params and len(params['category_ids']) > 0: 
      category_ids = params['category_ids']
      inicial_category_ids = category_ids
    if len(params['date_start']) > 0 and len(params['date_end']) > 0:
      date_start = params['date_start']
      date_end = params['date_end']

      inicial_date_start = date_string_to_datatime(date_start)
      inicial_date_end = date_string_to_datatime(date_end)

  data = total_expenses_and_incomes_values(date_start, date_end, user_ids, category_ids)

  value_expense = ([item['value'] for item in data if item['expense']])[0]

  value_income = ([item['value'] for item in data if not item['expense']])[0]

  value_percent = calculation_percent(value_income, value_expense)

  percent_progress_bar(frame_body, value_percent)

  income_and_expense_chart(frame_body, value_income, value_expense)

  income_and_expense_summary(frame_body, value_income, value_expense)

  search_criteria(frame_body, main_frame, inicial_date_start, inicial_date_end, user_ids, category_ids)

  list_transactions = list_transactions_values_expenses_to_categories(date_start, date_end, user_ids, category_ids)

  expense_pie_chart(frame_footer, list_transactions)
