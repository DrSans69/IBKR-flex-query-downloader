import tkinter as tk
from tkinter import ttk
import logging

from data import Credentials
import ibkr_reports


class App:
    def __init__(self, root: tk.Tk, creds: Credentials):
        self.creds = creds

        self.root = root
        self.root.title("IBKR Flex Queries Downloader")

        self.main_frame = tk.Frame(root)
        self.reports_frame = tk.Frame(root)
        self.credentials_frame = tk.Frame(root)
        self.credentials_add_frame = tk.Frame(root)

        self.setup_main_frame()
        self.setup_reports_frame()
        self.setup_credentials_frame()
        self.setup_credentials_add_frame()

        self.show_frame(self.main_frame)

    #
    def setup_main_frame(self):
        frame = self.main_frame

        tk.Label(frame, text="Welcome!",
                 font=("Arial", 16)).pack(pady=10)

        tk.Button(frame, text="Credentials",
                  command=lambda: self.show_frame(self.credentials_frame)).pack(pady=5)

        tk.Button(frame, text="Reports",
                  command=lambda: self.show_frame(self.reports_frame)).pack(pady=5)

    def setup_reports_frame(self):
        frame = self.reports_frame

        tk.Label(frame, text="Processing reports", font=("Arial", 14)).pack()

        tk.Button(frame, text="Start",
                  command=self.process_reports).pack(pady=10)

        tk.Button(frame, text="Go Back",
                  command=lambda: self.show_frame(self.main_frame)).pack(pady=10)

    def setup_credentials_frame(self):
        frame = self.credentials_frame

        tk.Label(frame, text="Select an item:",
                 font=("Arial", 14)).pack(pady=5)

        self.tree = ttk.Treeview(frame, columns=(
            "col1", "col2", "col3"), show="headings")
        self.tree.heading("col1", text="Name")
        self.tree.heading("col2", text="Token")
        self.tree.heading("col3", text="Query_id")

        for name, cred in self.creds.items():
            self.tree.insert("", tk.END, values=(
                name, cred.token, cred.query_id))

        self.tree.pack(fill="both", expand=True)

        tk.Button(frame, text="Add credential", command=lambda: self.show_frame(
            self.credentials_add_frame)).pack(pady=10)

        tk.Button(frame, text="Remove credential",
                  command=lambda: self.remove_credential_from_tree(self.tree)).pack(pady=5)

        tk.Button(frame, text="Go Back",
                  command=lambda: self.show_frame(self.main_frame)).pack(pady=10)

    def setup_credentials_add_frame(self):
        frame = self.credentials_add_frame

        tk.Label(frame, text="Name:").grid(
            row=0, column=0, sticky="e", padx=5, pady=5)

        name_input = tk.Entry(frame)
        name_input.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Token:").grid(
            row=1, column=0, sticky="e", padx=5, pady=5)

        token_input = tk.Entry(frame)
        token_input.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Query id:").grid(
            row=2, column=0, sticky="e", padx=5, pady=5)

        query_id_input = tk.Entry(frame)
        query_id_input.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Save", command=lambda: self.add_credential(name_input.get(
        ), token_input.get(), query_id_input.get())).grid(row=3, column=0, padx=5, pady=10)

        tk.Button(frame, text="Cancel", command=lambda: self.show_frame(
            self.credentials_frame)).grid(row=3, column=1, padx=5, pady=10)

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
        self.refresh_tree()
        self.show_frame(self.credentials_frame)

    def add_credential(self, name: str, token: str, query_id: str):
        self.creds.add(name, token, query_id)
        self.creds.write()
        self.refresh_tree()
        self.show_frame(self.credentials_frame)

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for name, cred in self.creds.items():
            self.tree.insert("", tk.END, values=(
                name, cred.token, cred.query_id))

    def process_reports(self):
        ibkr_reports.process_reports(self.creds)


def run_app(creds: Credentials):
    root = tk.Tk()
    root.geometry("800x400")
    App(root, creds)
    root.mainloop()
