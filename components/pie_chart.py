import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_random_colors(n):
    return ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]

class PieChart:
    def __init__(self, frame_footer, list_transactions):
        self.frame_chart = tk.Frame(frame_footer, width=520, height=300, bg="white")
        self.frame_chart.grid(row=0, column=0, padx=10, sticky="nsew")

        self.frame_legend = tk.Frame(frame_footer, width=520, height=300, bg="white")
        self.frame_legend.grid(row=0, column=1, padx=10, sticky="nsew")

        self.canvas = tk.Canvas(self.frame_legend, bg="white")
        self.scroll_y = ttk.Scrollbar(self.frame_legend, orient="vertical", command=self.canvas.yview)
        self.legend_frame = tk.Frame(self.canvas, bg="white")

        self.canvas.create_window((0, 0), window=self.legend_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.legend_labels = []  # Armazena referências aos labels da legenda

        self.update_chart(list_transactions)

    def update_chart(self, list_transactions):
        categorias = [item[0] for item in list_transactions]
        values = [item[1] for item in list_transactions]
        colors = generate_random_colors(len(categorias))

        self.update_pie_chart(categorias, values, colors)
        self.update_pie_legend(categorias, values, colors)

    def update_pie_chart(self, categorias, values, colors):
        if hasattr(self, "figura"):
            self.figura.clear()  # Limpa a figura existente

        self.figura = plt.Figure(figsize=(5, 3), dpi=90)
        ax = self.figura.add_subplot(111)

        explode = [0.05] * len(categorias)
        ax.pie(values, explode=explode, wedgeprops=dict(width=0.3), colors=colors, shadow=True, startangle=90)

        if hasattr(self, "canva_categoria"):
            self.canva_categoria.get_tk_widget().destroy()  # Remove o canvas anterior

        self.canva_categoria = FigureCanvasTkAgg(self.figura, self.frame_chart)
        self.canva_categoria.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canva_categoria.draw()

    def update_pie_legend(self, categorias, values, colors):
        total_value = sum(values) if sum(values) > 0 else 1  # Evita divisão por zero
        percentages = [(value / total_value) * 100 for value in values]

        legenda = [
            f"{categoria} - R${value:.2f} - {percentage:.1f}%"
            for categoria, value, percentage in zip(categorias, values, percentages)
        ]

        # Remover labels antigos
        for label in self.legend_labels:
            label.destroy()

        self.legend_labels.clear()

        # Criar novos labels
        for text, color in zip(legenda, colors):
            frame_item = tk.Frame(self.legend_frame, bg="white")
            frame_item.pack(fill=tk.X, pady=2)

            color_box = tk.Label(frame_item, bg=mcolors.to_hex(color), width=2, height=1)
            color_box.pack(side=tk.LEFT, padx=5)

            label = tk.Label(frame_item, text=text, bg="white", anchor="w")
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            self.legend_labels.append(frame_item)  # Armazena referência

        self.legend_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


# Criando a interface principal
#root = tk.Tk()
#root.title("Gráfico de Pizza com Legenda Atualizável")
#root.geometry("1100x600")
#
#frame_footer = tk.Frame(root)
#frame_footer.pack(pady=20, fill=tk.BOTH, expand=True)
#
## Criando a instância do gráfico
#list_transactions = [
#    ("Alimentação", 500),
#    ("Transporte", 300),
#    ("Lazer", 200),
#]
#chart = ExpensePieChart(frame_footer, list_transactions)
#
## Função para atualizar os valores do gráfico
#def atualizar_grafico():
#    categorias = ["Alimentação", "Transporte", "Lazer", "Saúde", "Educação"]
#    new_data = [(cat, random.randint(100, 1000)) for cat in categorias]
#    chart.update_chart(new_data)
#
## Botão para atualizar os dados
#btn_atualizar = tk.Button(root, text="Atualizar Dados", command=atualizar_grafico)
#btn_atualizar.pack(pady=10)
#
#root.mainloop()
