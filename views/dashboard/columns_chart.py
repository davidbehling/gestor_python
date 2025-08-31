import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ..colors import colors


# ===========================
# Gráfico - Colunas de Barras
# ===========================

def income_and_expense_chart(frame, income, expense):
  categories = ['Renda', 'Despesas', 'Saldo']
  values = [income, expense, (income - expense)]

  figura = plt.Figure(figsize=(4, 3.45), dpi=60)

  ax = figura.add_subplot(111)
  ax.bar(categories, values,  color=colors, width=0.9)

  c = 0

  for i in ax.patches:
      ax.text(i.get_x()-.001, i.get_height()+.5,
              str("{:,.0f}".format(values[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom', color='dimgrey')
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

  canva = FigureCanvasTkAgg(figura, frame)
  canva.get_tk_widget().place(x=10, y=70)