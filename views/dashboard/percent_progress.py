import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Progressbar
from ..colors import *


# ============================
# Gráfico - Barra de Progresso
# ============================

def percent_progress_bar(frame, value):
  # Título.
  label_name = tk.Label(frame, text='Porcentagem da receita gasta', height=1, anchor=tk.NW, font=('Verdana 12'), bg=co1, fg=co4)
  label_name.place(x=7, y=5)

  # Barra de Progresso.
  styles = ttk.Style()
  styles.theme_use('default')
  styles.configure('black.Horizontal.TProgressbar', background='#daed6b')
  styles.configure('TProgressbar', thickness=25)

  bar = Progressbar(frame, length=180, style='black.Horizontal.TProgressbar')
  bar.place(x=10, y=35)
  bar['value'] = value

  # Valor percentual exibido ao lado da barra de progresso.
  label_percent = tk.Label(frame, text="{:,.2f}%".format(value), anchor=tk.NW, font=('Verdana 12'), bg=co1, fg=co4)
  label_percent.place(x=200, y=35)
