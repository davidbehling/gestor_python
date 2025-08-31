import tkinter as tk
from tkinter import ttk

class MultiSelectCombobox(ttk.Entry):
    def __init__(self, parent, objects, display_property, value_property, initial_values=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.objects = objects
        self.display_property = display_property
        self.value_property = value_property
        self.selected_values = set()
        self.var = tk.StringVar()
        self.var.set("Selecione")
        self.configure(textvariable=self.var, state="readonly")

        self.window = None  # Janela que conterá a lista suspensa
        self.listbox = None
        self.scrollbar = None
        self.options_vars = {}

        # Inicializa a lista de opções
        for obj in objects:
            display_value = getattr(obj, display_property)
            self.options_vars[display_value] = (tk.BooleanVar(value=False), obj)

        # Define os valores iniciais, se fornecidos
        if initial_values:
            self.set_initial_values(initial_values)

        # Evento para abrir o menu ao clicar no Entry
        self.bind("<Button-1>", self.show_menu)

    def show_menu(self, event):
        """Exibe a lista suspensa com até 10 itens visíveis e rolagem, se necessário."""
        if self.window:
            self.window.destroy()

        self.window = tk.Toplevel(self)
        self.window.wm_overrideredirect(True)  # Remove bordas
        self.window.geometry(f"200x200+{self.winfo_rootx()}+{self.winfo_rooty() + self.winfo_height()}")
        self.window.transient(self.parent)

        # Criar Listbox com Scrollbar se necessário
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, height=min(10, len(self.objects)))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adiciona Scrollbar se houver mais de 10 itens
        if len(self.objects) > 10:
            self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Adiciona os itens na Listbox
        for obj in self.objects:
            display_value = getattr(obj, self.display_property)
            self.listbox.insert(tk.END, display_value)

        # Marca os itens previamente selecionados
        for i, obj in enumerate(self.objects):
            if obj in self.selected_values:
                self.listbox.select_set(i)

        # Evento de seleção
        self.listbox.bind("<<ListboxSelect>>", self.update_selection)

        # Fecha a janela ao perder o foco
        self.window.bind("<FocusOut>", lambda e: self.window.destroy())
        self.window.focus_set()

    def update_selection(self, event=None):
        """Atualiza os valores selecionados e o campo de entrada."""
        self.selected_values = {
            self.objects[i] for i in self.listbox.curselection()
        }
        self.update_entry()

    def update_entry(self):
        """Atualiza o texto exibido no campo de entrada."""
        if not self.selected_values:
            self.var.set("Selecione")
        else:
            display_names = [getattr(obj, self.display_property) for obj in self.selected_values]
            display_text = ", ".join(display_names)
            if len(display_text) > 30:
                display_text = display_text[:27] + "..."
            self.var.set(display_text)

    def get_selected_values(self):
        """Retorna os valores das propriedades configuradas para o resultado."""
        return [getattr(obj, self.value_property) for obj in self.selected_values]

    def set_initial_values(self, initial_values):
        """Define os valores iniciais selecionados."""
        for obj in self.objects:
            if getattr(obj, self.value_property) in initial_values:
                self.selected_values.add(obj)
        self.update_entry()


# Exemplo de classe de objetos
#class Item:
#    def __init__(self, id, name):
#        self.id = id
#        self.name = name
#
## Lista de objetos
#objects = [
#  Item(i, f"Item {i}") for i in range(1, 16)
#]
#
#root = tk.Tk()
#combobox = MultiSelectCombobox(
#    root,
#    objects=objects,
#    display_property="name",
#    value_property="id",
#    initial_values=[1, 3]
#)
#combobox.pack(pady=20)
#root.mainloop()
