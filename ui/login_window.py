import tkinter as tk
from tkinter import ttk, messagebox

class loginWindow:
    def __init__(self, root, on_success_callback):
        self.root=root
        self.on_success_callback=on_success_callback
        