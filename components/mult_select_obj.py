import tkinter as tk
from tkinter import ttk

class MultiSelectCombobox(ttk.Entry):
    def __init__(self, parent, objects, display_property, value_property, *args, **kwargs):
        """
        Combobox com seleção múltipla que permite exibir e obter propriedades específicas de objetos.

        :param parent: Widget pai.
        :param objects: Lista de objetos/dicionários.
        :param display_property: Propriedade que será exibida na lista.
        :param value_property: Propriedade que será retornada como resultado.
        """
        super().__init__(parent, *args, **kwargs)
        self.objects = objects
        self.display_property = display_property
        self.value_property = value_property

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
        for obj in objects:
            display_value = getattr(obj, display_property)
            var = tk.BooleanVar(value=False)
            self.options_vars[display_value] = (var, obj)
            self.menu.add_checkbutton(
                label=display_value,
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
            obj for display_value, (var, obj) in self.options_vars.items() if var.get()
        }
        self.update_entry()
        self.update_select_all()

    def toggle_all(self):
        """Marca ou desmarca todas as opções."""
        select_all = self.select_all_var.get()
        for var, _ in self.options_vars.values():
            var.set(select_all)
        self.update_selection()

    def update_select_all(self):
        """Atualiza o estado de "Marcar Todos/Desmarcar Todos"."""
        all_selected = len(self.selected_values) == len(self.objects)
        self.select_all_var.set(all_selected)

    def update_entry(self):
        """Atualiza o texto exibido no campo de entrada."""
        if not self.selected_values:
            self.var.set("Selecione")
        else:
            display_names = [getattr(obj, self.display_property) for obj in self.selected_values]
            display_text = ", ".join(display_names)
            if len(display_text) > 30:  # Limita o tamanho do texto no input
                display_text = display_text[:27] + "..."
            self.var.set(display_text)

    def get_selected_values(self):
        """Retorna os valores das propriedades configuradas para o resultado."""
        return [getattr(obj, self.value_property) for obj in self.selected_values]


## Exemplo de uso
#class Category:
#    def __init__(self, id, name, expense):
#        self.id = id
#        self.name = name
#        self.expense = expense
#
#    def __repr__(self):
#        return f"<Category(id={self.id}, name='{self.name}', expense={self.expense})>"
#
#
#if __name__ == "__main__":
#    root = tk.Tk()
#    root.title("Combobox com Multi Seleção")
#
#    # Dados de exemplo
#    categories = [
#        Category(9, "Combustível", True),
#        Category(7, "Desnecessário", True),
#        Category(6, "Diversos", True),
#        Category(4, "Farmácia", True),
#        Category(5, "Lanches", True),
#        Category(1, "Mercado", True),
#        Category(2, "Padaria", True),
#        Category(3, "Verdureira", True),
#        Category(8, "Vestuário", True),
#    ]
#
#    # Criação do Combobox com múltipla seleção
#    multi_combobox = MultiSelectCombobox(
#        root,
#        objects=categories,
#        display_property="name",
#        value_property="id",
#        width=30
#    )
#    multi_combobox.pack(padx=10, pady=10)
#
#    # Botão para exibir os valores selecionados
#    def show_selections():
#        print(f"IDs selecionados: {multi_combobox.get_selected_values()}")
#
#    btn = ttk.Button(root, text="Mostrar Seleções", command=show_selections)
#    btn.pack(padx=10, pady=10)
#
#    root.mainloop()
