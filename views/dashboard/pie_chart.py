import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ..colors import *

def generate_random_colors(n):
    return ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]

def expense_pie_chart(frame_footer, list_transactions):
  frame_chart = tk.Frame(frame_footer, width=520, height=300, bg=co1)
  frame_chart.grid(row=0, column=0, padx=10, sticky="nsew")

  frame_legend = tk.Frame(frame_footer, width=520, height=300, bg=co1)
  frame_legend.grid(row=0, column=1, padx=10, sticky="nsew")

  result = list_transactions
  categorias = [item[0] for item in result]
  values = [item[1] for item in result]  

  colors = generate_random_colors(max(len(categorias), 100))

  pie_chart(frame_chart, categorias, values, colors)
  pie_legend(frame_legend, categorias, values, colors)


def pie_chart(frame_chart, categorias, values, colors):
  figura = plt.Figure(figsize=(5, 3), dpi=90)
  ax = figura.add_subplot(111)

  explode = [0.05] * len(categorias)
  ax.pie(
    values,
    explode=explode,
    wedgeprops=dict(width=0.3),
    colors=colors,
    shadow=True,
    startangle=90
  )

  canva_categoria = FigureCanvasTkAgg(figura, frame_chart)
  canva_categoria.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


def pie_legend(frame_legend, categorias, values, colors):
  # Criar canvas com barra de rolagem para a legenda
  canvas = tk.Canvas(frame_legend, bg="white")
  scroll_y = ttk.Scrollbar(frame_legend, orient="vertical", command=canvas.yview)
  legend_frame = tk.Frame(canvas, bg="white")

  total_value = sum(values)

  # Calculando porcentagens
  percentages = [(value / total_value) * 100 for value in values]

  # Configurando a legenda
  legenda = [
      f"{categoria} - R${value:.2f} - {percentage:.1f}%"
      for categoria, value, percentage in zip(categorias, values, percentages)
  ]

  # Configurar scroll no canvas
  legend_frame.bind(
      "<Configure>",
      lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
  )

  canvas.create_window((0, 0), window=legend_frame, anchor="nw")
  canvas.configure(yscrollcommand=scroll_y.set)

  # Adicionar a legenda no legend_frame com as cores
  for text, color in zip(legenda, colors):
    frame_item = tk.Frame(legend_frame, bg="white")
    frame_item.pack(fill=tk.X, pady=2)

    # Corrigido: uso de mcolors para converter a cor
    color_box = tk.Label(frame_item, bg=mcolors.to_hex(color), width=2, height=1)
    color_box.pack(side=tk.LEFT, padx=5)

    label = tk.Label(frame_item, text=text, bg="white", anchor="w")
    label.pack(side=tk.LEFT, fill=tk.X, expand=True)

  # Posicionar canvas e scrollbar
  canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
  scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
