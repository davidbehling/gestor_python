import tkinter as tk
from tkinter import ttk

from views.categories.categories import categories_init
from views.banks.banks import banks_init
from views.dashboard.dashboard_new import dashboard_init_new
from views.expenses.expenses import expenses_init
from views.exports.exports import exports_init
from views.imports.imports import imports_init
from views.incomes.incomes import incomes_init
from views.payments.payments import payments_init
from views.users.users import users_init

from global_values import windown_geometry

# Função para alternar o conteúdo da interface com base no ícone selecionado
def change_frame(content, args=None):
    # Remover widgets adicionados com .pack()
    for widget in main_frame.pack_slaves():
        widget.destroy()

    # Remover widgets adicionados com .grid()
    for widget in main_frame.grid_slaves():
        widget.destroy()

    # Remover qualquer outro widget (como os posicionados com .place())
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Atualiza a interface antes de iniciar a tarefa pesada
    main_frame.update_idletasks() 

    # Adiciona conteúdo de acordo com o ícone selecionado
    if content == "dashboard":
        dashboard_init_new(main_frame, args)
    elif content == "expenses":
        expenses_init(main_frame, args)
    elif content == "incomes":
        incomes_init(main_frame, args)
    elif content == "users":
        users_init(main_frame, args)
    elif content == "categories":
        categories_init(main_frame, args)
    elif content == "account_banks":
        banks_init(main_frame, args)
    elif content == "payments":
        payments_init(main_frame, args)
    elif content == "imports":
        imports_init(main_frame, args)
    elif content == "exports":
        exports_init(main_frame, args)

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Gerenciamento")
root.geometry(windown_geometry)

# Frame lateral para os ícones
side_frame = tk.Frame(root, width=200, bg="#2c3e50")
side_frame.pack(side="left", fill="y")

# Botões de ícones na barra lateral
buttons = [
    ("Dashboard", "dashboard"),
    ("Despesas", "expenses"),
    ("Receitas", "incomes"),
    ("Usuários", "users"),
    ("Categorias", "categories"),
    ("Bancos", "account_banks"),
    ("Tipos de Pagamentos", "payments"),
    ("Importação", "imports"),
    ("Exportação", "exports"),
]

for text, frame in buttons:
    btn = tk.Button(side_frame, text=text, font=("Arial", 12), bg="#34495e", fg="white",
                    relief="flat", command=lambda c=frame: change_frame(c))
    btn.pack(fill="x", pady=5, padx=10)

# Frame principal para exibir conteúdo dinâmico
main_frame = tk.Frame(root, bg="#ecf0f1")
main_frame.pack(side="right", expand=True, fill="both")

# Conteúdo inicial
change_frame("dashboard")

# Inicia o loop da interface gráfica
root.mainloop()
