import tkinter as tk
from tkinter import ttk

class MultiSelectCombobox(ttk.Entry):
    def __init__(self, parent, objects, display_property, value_property, initial_values=None, *args, **kwargs):
        """
        Combobox com seleção múltipla que permite exibir e obter propriedades específicas de objetos.

        :param parent: Widget pai.
        :param objects: Lista de objetos/dicionários.
        :param display_property: Propriedade que será exibida na lista.
        :param value_property: Propriedade que será retornada como resultado.
        :param initial_values: Lista de valores iniciais para seleção.
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

        # Define os valores iniciais, se fornecidos
        if initial_values:
            self.set_initial_values(initial_values)

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

    def set_initial_values(self, initial_values):
        """
        Define os valores iniciais selecionados.
        :param initial_values: Lista de valores correspondentes à propriedade value_property.
        """
        for obj in self.objects:
            if getattr(obj, self.value_property) in initial_values:
                display_value = getattr(obj, self.display_property)
                var, _ = self.options_vars[display_value]
                var.set(True)
                self.selected_values.add(obj)
        self.update_entry()
        self.update_select_all()
    
    def add_objects(self, new_objects, initial_values=None):
        """
        Adiciona novos objetos ao combobox e atualiza o menu de seleção.
        
        :param new_objects: Lista de novos objetos a serem adicionados.
        :param initial_values: Lista de valores correspondentes à propriedade value_property para pré-seleção.
        """
        for obj in new_objects:
            if obj in self.objects:
                continue  # Evita adicionar duplicados
            
            self.objects.append(obj)
            display_value = getattr(obj, self.display_property)
            
            # Cria a variável e adiciona ao menu
            var = tk.BooleanVar(value=False)
            self.options_vars[display_value] = (var, obj)
            self.menu.add_checkbutton(
                label=display_value,
                variable=var,
                command=self.update_selection
            )

            # Pré-seleção, se aplicável
            if initial_values and getattr(obj, self.value_property) in initial_values:
                var.set(True)
                self.selected_values.add(obj)
        
        # Atualiza o campo de entrada e o estado de "Marcar Todos"
        self.update_entry()
        self.update_select_all()

    def reset_objects(self, new_objects, initial_values=None):
        """
        Limpa a listagem atual e adiciona novos objetos ao combobox.
        
        :param new_objects: Lista de novos objetos a serem adicionados.
        :param initial_values: Lista de valores correspondentes à propriedade value_property para pré-seleção.
        """
        # Limpa o estado atual
        self.objects = []
        self.selected_values = set()
        self.options_vars = {}

        # Remove todas as opções do menu
        self.menu.delete(2, "end")  # Remove tudo após o separador

        # Atualiza a lista com os novos objetos
        self.add_objects(new_objects, initial_values)



# Exemplo de classe de objetos
#class Item:
#    def __init__(self, id, name):
#        self.id = id
#        self.name = name
#
## Lista de objetos
#objects = [Item(1, "Item 1"), Item(2, "Item 2"), Item(3, "Item 3")]
#
#root = tk.Tk()
#combobox = MultiSelectCombobox(
#    root,
#    objects=objects,
#    display_property="name",
#    value_property="id",
#    initial_values=[1, 3]
#)
#combobox.pack()
#root.mainloop()
