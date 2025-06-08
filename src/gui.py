import tkinter as tk
import tkinter.scrolledtext
from tkinter import ttk
from typing import Callable
import threading
import copy

import src.core as core
from src.data import Credentials
from src.my_logging import TkinterHandler


class App:
    def __init__(self, root: tk.Tk, creds: Credentials):
        self.creds = creds

        self.root = root
        self.root.title("IBKR Flex Queries Downloader")

        self.main_frame = MainFrame(root, self)
        self.reports_frame = ReportsFrame(root, self)
        self.credentials_frame = CredentialsFrame(root, self)
        self.credentials_add_frame = CredentialsAddFrame(root, self)

        self.show_frame(self.main_frame)

    #
    def show_frame(self, frame: tk.Frame):
        self.hide_all_frames()
        frame.pack()
        self.root.update_idletasks()

    def hide_all_frames(self):
        self.main_frame.pack_forget()
        self.reports_frame.pack_forget()
        self.credentials_frame.pack_forget()
        self.credentials_add_frame.pack_forget()

    #
    def remove_credential_from_tree(self, tree):
        selection = tree.selection()
        if not selection:
            return

        name = tree.item(selection[0])['values'][0]

        self.creds.remove(name)
        self.creds.write()
        self.refresh_tree(tree)
        self.show_frame(self.credentials_frame)

    def add_credential(self, name: str, token: str, query_id: str):
        self.creds.add(name, token, query_id)
        self.creds.write()
        self.refresh_tree(self.credentials_frame.tree)
        self.show_frame(self.credentials_frame)

    def refresh_tree(self, tree):
        for item in self.credentials_frame.tree.get_children():
            tree.delete(item)

        for name, cred in self.creds.items():
            tree.insert(
                "",
                tk.END,
                values=(name, cred.token, cred.query_id)
            )

    def process_reports(self):
        core.process_reports(self.creds)


class MainFrame(tk.Frame):
    def __init__(self, master: tk.Tk, parent: App):
        super().__init__(master)

        tk.Label(
            self,
            text="Welcome!",
            font=("Arial", 16)
        ).pack(pady=10)

        tk.Button(
            self,
            text="Reports",
            width=10,
            command=lambda: parent.show_frame(parent.reports_frame)
        ).pack(pady=5)

        tk.Button(
            self,
            text="Credentials",
            width=10,
            command=lambda: parent.show_frame(parent.credentials_frame)
        ).pack(pady=5)

        tk.Button(
            self,
            text="Exit",
            width=10,
            command=parent.root.destroy
        ).pack(pady=5)


class ReportsFrame(tk.Frame):
    def __init__(self, master: tk.Tk, parent: App):
        super().__init__(master)

        self.text_widget = tkinter.scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            height=15
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        TkinterHandler(self.text_widget)

        tk.Button(
            self,
            text="Start",
            command=lambda: threading.Thread(
                target=core.process_reports,
                args=(copy.deepcopy(parent.creds),),
                daemon=True
            ).start()
        ).pack(pady=10)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: parent.show_frame(parent.main_frame)
        ).pack(pady=10)


class CredentialsFrame(tk.Frame):
    def __init__(self, master: tk.Tk, parent: App):
        super().__init__(master)

        tk.Label(
            self,
            text="Select an item:",
            font=("Arial", 14)
        ).pack(pady=5)

        tree = ttk.Treeview(
            self,
            columns=("col1", "col2", "col3"),
            show="headings"
        )
        tree.heading("col1", text="Name")
        tree.heading("col2", text="Token")
        tree.heading("col3", text="Query_id")

        for name, cred in parent.creds.items():
            tree.insert(
                "",
                tk.END,
                values=(name, cred.token, cred.query_id)
            )

        tree.pack(fill="both", expand=True)

        self.tree = tree

        tk.Button(
            self,
            text="Add credential",
            command=lambda: parent.show_frame(parent.credentials_add_frame)
        ).pack(pady=10)

        tk.Button(
            self,
            text="Remove credential",
            command=lambda: parent.remove_credential_from_tree(self.tree)
        ).pack(pady=5)

        tk.Button(
            self,
            text="Go Back",
            command=lambda: parent.show_frame(parent.main_frame)
        ).pack(pady=10)


class CredentialsAddFrame(tk.Frame):
    def __init__(self, master: tk.Tk, parent: App):
        super().__init__(master)

        tk.Label(
            self,
            text="Name:"
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)

        name_input = tk.Entry(self)
        name_input.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            self,
            text="Token:"
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)

        token_input = tk.Entry(self)
        token_input.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(
            self,
            text="Query id:"
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)

        query_id_input = tk.Entry(self)
        query_id_input.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(
            self,
            text="Cancel",
            command=lambda: parent.show_frame(parent.credentials_frame)
        ).grid(row=3, column=0, padx=5, pady=5)

        tk.Button(
            self,
            text="Save",
            width=10,
            height=1,
            command=lambda: parent.add_credential(
                name_input.get(),
                token_input.get(),
                query_id_input.get()
            )
        ).grid(row=3, column=1, padx=10, pady=10)


def run_gui(creds: Credentials):
    root = tk.Tk()
    App(root, creds)
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    root.focus_force()
    root.geometry("600x400")
    root.mainloop()
