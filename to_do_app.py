import tkinter as tk
from Todo_Service_Class import Todo_Service_Class
from Todo_Data import TodoDataclass
from to_do_item import ToDoItemFrame


class ToDoTk(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("To-Do-Liste")
        self.minsize(400,400)
        self.geometry("400x400")

        # Datenbank

        self.service = Todo_Service_Class()

        # Top-Leiste
        self.top_leiste = tk.Frame(master=self, bg="#ffeead")
        self.top_leiste.pack(side="top", fill="x")

        # Eingabefeld
        label = tk.Label(                   #Label für Top-Leiste
            master=self.top_leiste,
            text="Was gibt's zu tun?",
            bg="#ffeead",
            fg="#ff6f69",
            font=("Bahnschrift SemiLight Condensed", 16, "bold"))
        label.pack(
            side="top",
            fill="both",
            padx="10",
            pady="10")

        # Checkbox-Counter
        self.checkbox_label = tk.Label(master=self.top_leiste, text="Erledigt:")
        self.checkbox_label.pack(side="bottom", fill="both", padx="10", pady="10")

        self.entry = tk.Entry(
            master=self.top_leiste,
            width=30)
        self.entry.pack(
            side="left",
            padx="10")
        self.entry.bind("<Return>", self.add_entry_event)           #Enter soll hinzufügen

        # Hinzufügen-Button
        add_button = tk.Button(
            master=self.top_leiste,
            text="Hinzufügen",
            command=self.add_entry)
        add_button.pack(
            side="left",
            pady="10")

        # Canvas für Listen-Container mit Scrollbar

        self.canvas = tk.Canvas(self, bg="#96ceb4")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(master=self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Listen-Container
        self.todoliste = tk.Frame(master=self.canvas,bg="#96ceb4")
        self.window_id = self.canvas.create_window((0,0), window=self.todoliste, anchor="n") #Fügt Frame in Canvas ein

        self.todoliste.bind("<Configure>", self.update_scrollregion)
        self.canvas.bind("<Configure>", self.center_window)

        # Alte Todos laden
        self.load_todos()

    def load_todos(self):
        for todo in self.service.get_all_todos():
            self.add_todo_frame(todo)
        self.update_count()
        self.update()

    def add_entry_event(self, event):       #Event-Handler für Enter-Taste
        self.add_entry()

    def add_entry(self):                    #Prüft Eingabe und fügt ggf. neue Karte hinzu
        todo = self.entry.get().strip()     #Strip() entfernt Leerzeichen vor oder nach der Eingabe
        if not todo:
            return                          #nichts tun bei leerem Eintrag
        todo = todo.capitalize()
        self.service.add_todo(todo)
        todos = self.service.get_all_todos()
        new_todo = todos[-1]               # -1 bedeutet, der zuletzt gespeicherte Eintrag
        self.add_todo_frame(new_todo)

        self.entry.delete(0, tk.END)
        self.update_count()

    def add_todo_frame(self, todo: TodoDataclass):                    #Erzeugt ein neues ToDo
        ein_frame = ToDoItemFrame(
            master=self.todoliste,
            todo=todo,
            on_toggle=self.toggle_done,
            on_delete=self.delete_todo)
        ein_frame.pack(fill="x", pady=4)

    def toggle_done(self, todo_id, done):
        self.service.update_todo_status(todo_id, done)
        self.update_count()

    def delete_todo(self, todo_id):
        self.service.delete_todo(todo_id)
        self.update_count()

    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def center_window(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.window_id, width=canvas_width)  # damit der Frame immer Canvas-Breite hat
        self.canvas.coords(self.window_id, canvas_width / 2, 0)     # x = Mitte, y = 0

    def update_count(self):
        count = 0
        for child in self.todoliste.winfo_children():
            if isinstance(child, ToDoItemFrame):
                if child.var.get() == 1:
                    count += 1
        self.checkbox_label.config(text=f"Erledigt: {count}")

