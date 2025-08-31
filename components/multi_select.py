import tkinter as tk
from tkinter import ttk

class MultiSelectCombobox(ttk.Entry):
    def __init__(self, parent, options, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.options = options
        self.selected_values = set()
        self.var = tk.StringVar()
        self.var.set("Selecione")
        self.configure(textvariable=self.var, state="readonly")

        # Criação do menu para seleção múltipla
        self.menu = tk.Menu(parent, tearoff=0)
        
        # Adiciona a opção de "Marcar Todos/Desmarcar Todos"
        self.select_all_var = tk.BooleanVar(value=False)
        self.menu.add_checkbutton(
            label="Marcar Todos", 
            variable=self.select_all_var, 
            command=self.toggle_all
        )
        self.menu.add_separator()

        # Adiciona as opções individuais
        self.options_vars = {}
        for option in options:
            var = tk.BooleanVar(value=False)
            self.options_vars[option] = var
            self.menu.add_checkbutton(
                label=option, 
                variable=var, 
                command=self.update_selection
            )

        # Evento para abrir o menu ao clicar no Entry
        self.bind("<Button-1>", self.show_menu)

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def update_selection(self):
        """Atualiza os valores selecionados e o campo de entrada."""
        self.selected_values = {
            option for option, var in self.options_vars.items() if var.get()
        }
        self.update_entry()
        self.update_select_all()

    def toggle_all(self):
        """Marca ou desmarca todas as opções."""
        select_all = self.select_all_var.get()
        for var in self.options_vars.values():
            var.set(select_all)
        self.update_selection()

    def update_select_all(self):
        """Atualiza o estado de "Marcar Todos/Desmarcar Todos"."""
        all_selected = len(self.selected_values) == len(self.options)
        self.select_all_var.set(all_selected)

    def update_entry(self):
        """Atualiza o texto exibido no campo de entrada."""
        if not self.selected_values:
            self.var.set("Selecione")
        else:
            display_text = ", ".join(self.selected_values)
            if len(display_text) > 30:  # Limita o tamanho do texto no input
                display_text = display_text[:27] + "..."
            self.var.set(display_text)

    def get_selected_values(self):
        """Retorna os valores selecionados."""
        return list(self.selected_values)

    def get_selected_ids(self, mapping):
        """Converte os nomes selecionados em IDs com base em um mapeamento."""
        return [mapping[name] for name in self.selected_values]


# Exemplo de uso
#if __name__ == "__main__":
#    root = tk.Tk()
#    root.title("Combobox com Multi Seleção")
#
#    # Opções e mapeamento de IDs
#    options = ["Opção 1", "Opção 2", "Opção 3", "Opção 4", "Opção 5"]
#    option_to_id = {f"Opção {i+1}": i+1 for i in range(len(options))}
#
#    # Criação do Combobox com múltipla seleção
#    multi_combobox = MultiSelectCombobox(root, options, width=30)
#    multi_combobox.pack(padx=10, pady=10)
#
#    # Botão para exibir os valores selecionados
#    def show_selections():
#        print(f"Valores selecionados: {multi_combobox.get_selected_values()}")
#        print(f"IDs selecionados: {multi_combobox.get_selected_ids(option_to_id)}")
#
#    btn = ttk.Button(root, text="Mostrar Seleções", command=show_selections)
#    btn.pack(padx=10, pady=10)
#
#    root.mainloop()
