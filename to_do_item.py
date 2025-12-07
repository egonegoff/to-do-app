import tkinter as tk

class ToDoItemFrame(tk.Frame):
    def __init__(self, master=None, todo=None, on_toggle=None, on_delete=None):
        super().__init__(master=master, padx=10, pady=5, bg="#ffcc5c")

        self.todo = todo
        self.on_toggle = on_toggle  # Callback für das Anklicken
        self.on_delete = on_delete  # Callback für das Löschen

        # Checkbox links
        self.var = tk.IntVar(value=1 if todo.done else 0)
        self.checkbutton = tk.Checkbutton(master=self, variable=self.var, command=self.checkbox_counter)
        self.checkbutton.pack(side="left", padx=(5, 10))

        # Label mittig
        self.label = tk.Label(master=self, text=todo.text, bg="#ffcc5c")
        self.label.pack(side="left", fill="x", expand=True)

        # Erledigte Todos durchstreichen
        if self.todo.done:
            self.label.config(fg="gray", font=("Bahnschrift SemiLight Condensed", 12, "overstrike"))
        else:
            self.label.config(fg="black", font=("Bahnschrift SemiLight Condensed", 12))

        # Löschen-Button rechts
        self.delete_button = tk.Button(
            master=self,
            text="Löschen",
            command=self.delete_self)
        self.delete_button.pack(side="right", padx=(10, 5))

    def checkbox_counter(self):
        if self.var.get() == 1:
            self.label.config(fg="gray", font=("Bahnschrift SemiLight Condensed", 12, "overstrike"))
        else:
            self.label.config(fg="black", font=("Bahnschrift SemiLight Condensed", 12))


        if self.on_toggle:
            self.on_toggle(self.todo.id, bool(self.var.get()))

    def delete_self(self):  # Löscht die Karte
        if self.on_delete:
            self.on_delete(self.todo.id)
        self.destroy()