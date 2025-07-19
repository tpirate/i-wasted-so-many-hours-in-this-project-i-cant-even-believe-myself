import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
import time

DATA_FILE = "projects.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class HoursWastedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hours Wasted")
        self.root.geometry("400x380")  # Increased height for visibility

        self.projects = load_data()
        initial_project = next(iter(self.projects), "")
        self.project_var = tk.StringVar(value=initial_project)
        self.time_var = tk.StringVar(value="Hours: 0.0")

        self.current_project = None
        self.start_time = None
        self.running = False
        self.last_saved_time = None

        self.full_widgets = []
        self.compact_widgets = []

        self.setup_ui()

    def setup_ui(self):
        # Full UI widgets
        lbl_select = tk.Label(self.root, text="Select Project:")
        lbl_select.pack(padx=20, pady=10)
        self.full_widgets.append(lbl_select)

        project_names = list(self.projects.keys()) or ["No Projects"]
        self.project_menu = tk.OptionMenu(self.root, self.project_var, *project_names)
        self.project_menu.pack(padx=20, pady=10)
        self.full_widgets.append(self.project_menu)

        btn_load = tk.Button(self.root, text="Load Project", command=self.load_project)
        btn_load.pack(padx=20, pady=5)
        self.full_widgets.append(btn_load)

        btn_new = tk.Button(self.root, text="New Project", command=self.new_project)
        btn_new.pack(padx=20, pady=5)
        self.full_widgets.append(btn_new)

        lbl_time = tk.Label(self.root, textvariable=self.time_var, font=("Arial", 18))
        lbl_time.pack(padx=20, pady=15)
        self.full_widgets.append(lbl_time)
        self.lbl_time = lbl_time  # For compact mode

        self.start_btn = tk.Button(self.root, text="Start", command=self.start_timer, state="disabled")
        self.start_btn.pack(padx=20, pady=5)
        self.full_widgets.append(self.start_btn)

        self.stop_btn = tk.Button(self.root, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_btn.pack(padx=20, pady=5)
        self.full_widgets.append(self.stop_btn)

        # Move Compact Mode button to the end for visibility
        btn_compact = tk.Button(self.root, text="Compact Mode", command=self.show_compact)
        btn_compact.pack(padx=40, pady=20)  # Extra padding for visibility
        self.full_widgets.append(btn_compact)

        # Compact UI widgets (initially hidden)
        btn_expand = tk.Button(self.root, text="X", command=self.show_full)

        self.compact_widgets.append(btn_expand)

    def refresh_project_menu(self):
        menu = self.project_menu["menu"]
        menu.delete(0, "end")
        for project in self.projects:
            menu.add_command(label=project, command=lambda p=project: self.project_var.set(p))

    def new_project(self):
        name = simpledialog.askstring("New Project", "Enter project name:")
        if name:
            if name in self.projects:
                messagebox.showerror("Error", "Project already exists.")
            else:
                self.projects[name] = 0.0
                save_data(self.projects)
                self.refresh_project_menu()
                self.project_var.set(name)

    def load_project(self):
        name = self.project_var.get()
        if name in self.projects:
            self.current_project = name
            self.time_var.set(f"Hours: {self.projects[name]:.2f}")
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
        else:
            messagebox.showerror("Error", "Please select a valid project.")

    def start_timer(self):
        if self.current_project:
            self.start_time = time.time()
            self.running = True
            self.last_saved_time = self.start_time
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.update_timer()

    def stop_timer(self):
        if self.running:
            elapsed = (time.time() - self.start_time) / 3600  # convert seconds to hours
            self.projects[self.current_project] += elapsed
            save_data(self.projects)
            self.time_var.set(f"Hours: {self.projects[self.current_project]:.2f}")
            self.running = False
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")

    def update_timer(self):
        if self.running:
            current_elapsed = (time.time() - self.start_time) / 3600
            total = self.projects[self.current_project] + current_elapsed
            self.time_var.set(f"Hours: {total:.2f}")

            # Auto-save every 60 seconds
            if time.time() - self.last_saved_time >= 60:
                self.projects[self.current_project] += (time.time() - self.start_time) / 3600
                self.start_time = time.time()  # reset start time
                save_data(self.projects)
                self.last_saved_time = self.start_time

            self.root.after(1000, self.update_timer)

    def show_compact(self):
        for w in self.full_widgets:
            w.pack_forget()
        self.lbl_time.pack(padx=15, pady=15)
        self.compact_widgets[0].pack(padx=20, pady=10)
        self.root.geometry("180x90")  # Much smaller window for compact mode

    def show_full(self):
        self.compact_widgets[0].pack_forget()
        for w in self.full_widgets:
            w.pack_configure()
        self.root.geometry("400x380")  # Restore to new taller size

if __name__ == "__main__":
    root = tk.Tk()
    app = HoursWastedApp(root)
    root.mainloop()
