import tkinter as tk
from ..colors import *


# =================
# Resumo financeiro
# =================

def income_and_expense_summary(frame, income, expense):
  categories = ['Total da Renda               ', 
                'Total de Despesas            ', 
                'Total de Saldo               ']

  values = [income, expense, (income - expense)]

  place_y = [[52, 35, 70], [132, 115, 150], [207, 190, 220]]

  for i in range(0, 3):
    l_line = tk.Label(frame, text='', width=215, height=1, anchor=tk.NW, font=('Arial 1'), bg='#545454')
    l_line.place(x=309, y=place_y[i][0])

    l_summary = tk.Label(frame, text=categories[i].upper(), anchor=tk.NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_summary.place(x=309, y=place_y[i][1])

    l_value = tk.Label(frame, text="R$ {:,.2f}".format(values[i]), anchor=tk.NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_value.place(x=309, y=place_y[i][2])