import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.append("..") 
from database import DataBase 
from ui.cat_page import CatPage
from languages import DB_MAPPING, get_display_text

class AdoptionPage:
    def __init__(self, app):
        self.app = app

    def apply_for_cat(self):
        selected = self.app.tree.selection()
        if not selected: return
        
        values = self.app.tree.item(selected)['values']
        cat_id = values[0]
        cat_name = values[1]
        display_status = values[5]
        
        db_status = DB_MAPPING.get(display_status, display_status)

        if db_status == "Tedavide":
            messagebox.showinfo("Info", self.app.t["msg_wait"])
            return
        elif db_status != "Barınakta":
            messagebox.showwarning("Warning", self.app.t["msg_invalid"])
            return

        confirm_msg = self.app.t["msg_confirm_app"].format(cat_name)
        if messagebox.askyesno("Confirm", confirm_msg):
            db = DataBase()
            db.apply_adoption(cat_id, self.app.current_user[0], lang=self.app.lang)            
            messagebox.showinfo("OK", self.app.t["msg_app_sent"])
            CatPage(self.app).show_cats()

    def show_applications(self):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=self.app.t["header_apps"], bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        
        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("cat_id", "cat_name", "breed", "applicant", "phone")
        self.app.app_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.app.app_tree.pack(fill="both", expand=True)
        
        self.app.app_tree.heading("cat_id", text="Cat ID")
        self.app.app_tree.heading("cat_name", text="Cat Name")
        self.app.app_tree.heading("breed", text="Breed")
        self.app.app_tree.heading("applicant", text="Applicant Name")
        self.app.app_tree.heading("phone", text="Phone")
        
        db = DataBase()
        apps = db.get_pending_applications()
        for app in apps: self.app.app_tree.insert("", tk.END, values=app)

        btn_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text=self.app.t["btn_approve"], style="Menu.TButton", command=lambda: self.process_app("approve")).pack(side="left", padx=10)
        ttk.Button(btn_frame, text=self.app.t["btn_reject"], style="Menu.TButton", command=lambda: self.process_app("reject")).pack(side="left", padx=10)

    def process_app(self, decision):
        selected = self.app.app_tree.selection()
        if not selected: return
        
        values = self.app.app_tree.item(selected)['values']
        cat_id = values[0]
        cat_name = values[1]
        applicant_name = values[3]
        
        db = DataBase()
        db.process_application(cat_id, decision, lang=self.app.lang)
        
        if decision == "approve":
            db.add_log(f"log_adopt|||{applicant_name}|||{cat_name}")
            messagebox.showinfo("Info", f"{cat_name} adopted!")
        elif decision == "reject":
            info = f"{applicant_name} - {cat_name}"
            db.add_log(f"log_app_rejected|||{info}")

        self.show_applications()

    def show_my_cats(self):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=self.app.t["header_my_cats"], bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        
        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        columns = ("id", "name", "breed", "age", "status")
        
        self.my_cats_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.my_cats_tree.pack(fill="both", expand=True)
        
        for col in columns: self.my_cats_tree.heading(col, text=col.capitalize())
        
        db = DataBase()
        my_cats = db.get_user_cats(self.app.current_user[0])
        
        for cat in my_cats:
            cat_list = list(cat)
            cat_list[2] = get_display_text(cat_list[2], self.app.lang) 
            cat_list[4] = get_display_text(cat_list[4], self.app.lang) 
            self.my_cats_tree.insert("", tk.END, values=cat_list)

        btn_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text=self.app.t["btn_health"], style="Menu.TButton", command=self.show_my_cat_health).pack()

    def show_my_cat_health(self):
        selected = self.my_cats_tree.selection()
        if not selected: return 

        values = self.my_cats_tree.item(selected)['values']
        cat_id = values[0]
        cat_name = values[1]

        db = DataBase()
        health_note = db.get_cat_health(cat_id)

        if not health_note or health_note.strip() == "":
            display_text = self.app.t["msg_no_health"]
        else:
            display_text = health_note

        messagebox.showinfo(f"{self.app.t['title_health']} - {cat_name}", display_text)