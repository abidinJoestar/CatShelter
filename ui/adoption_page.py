import tkinter as tk
from tkinter import ttk
import sys
sys.path.append("..") 
from database import DataBase 

class AdoptionPage:
    def __init__(self, app):
        self.app = app

    def apply_for_cat(self):
        selected = self.app.tree.selection()
        if not selected: return
        values = self.app.tree.item(selected)['values']
        cat_id, cat_name, status = values[0], values[1], values[5]

        if status == "Tedavide":
            from tkinter import messagebox
            messagebox.showinfo("Bilgi", "Bu kedi şu an tedavide.")
            return
        elif status != "Barınakta":
            from tkinter import messagebox
            messagebox.showwarning("Uyarı", "Bu kedi uygun değil.")
            return

        from tkinter import messagebox
        if messagebox.askyesno("Başvuru", f"{cat_name} için başvur?"):
            db = DataBase()
            db.apply_adoption(cat_id, self.app.current_user[0])
            messagebox.showinfo("Başarılı", "Başvuru alındı.")
            # Kedi listesine geri dönmek için CatPage kullanıyoruz
            from ui.cat_page import CatPage
            CatPage(self.app).show_cats()

    def show_applications(self):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text="Bekleyen Başvurular", bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        
        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("cat_id", "cat_name", "breed", "applicant", "phone")
        self.app.app_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.app.app_tree.pack(fill="both", expand=True)
        
        for col in columns: self.app.app_tree.heading(col, text=col)
        
        db = DataBase()
        apps = db.get_pending_applications()
        for app in apps: self.app.app_tree.insert("", tk.END, values=app)

        btn_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="ONAYLA ✅", style="Menu.TButton", command=lambda: self.process_app("approve")).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="REDDET ❌", style="Menu.TButton", command=lambda: self.process_app("reject")).pack(side="left", padx=10)

    def process_app(self, decision):
        selected = self.app.app_tree.selection()
        if not selected: return
        cat_id = self.app.app_tree.item(selected)['values'][0]
        DataBase().process_application(cat_id, decision)
        self.show_applications()

    def show_my_cats(self):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text="Sahiplendiğim Dostlarım", bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("id", "name", "breed", "age", "status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        tree.pack(fill="both", expand=True)
        for col in columns: tree.heading(col, text=col.capitalize())
        
        db = DataBase()
        my_cats = db.get_user_cats(self.app.current_user[0])
        for cat in my_cats: tree.insert("", tk.END, values=cat)