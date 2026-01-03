import tkinter as tk
from tkinter import ttk
import sys
sys.path.append("..") 
from database import DataBase 

class UserPage:
    def __init__(self, app):
        self.app = app

    def show_personnel(self):
        self.show_user_list(self.app.t["menu_personnel"], DataBase().get_all_personnel())

    def show_customers(self):
        self.show_user_list(self.app.t["menu_customer"], DataBase().get_all_customers(), is_customer=True)

    def show_user_list(self, user_type, data, is_customer=False):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=user_type, bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)

        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ["id", "fullname", "username", "phone", "password"]
        if is_customer: columns.append("cats")

        self.app.user_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.app.user_tree.pack(fill="both", expand=True)

        for col in columns: 
            self.app.user_tree.heading(col, text=col.capitalize())
            
        if data:
            for item in data:
                if is_customer:
                    l = list(item)
                    if len(l) > 5 and l[5] is None: l[5] = "-"
                    self.app.user_tree.insert("", tk.END, values=l)
                else:
                    self.app.user_tree.insert("", tk.END, values=item)

        btn_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        btn_frame.pack(pady=10)
        
        cmd_add = self.add_customer_form if is_customer else self.add_personnel_form
        cmd_del = self.delete_customer if is_customer else self.delete_personnel
        cmd_upd = self.open_customer_update if is_customer else self.open_personnel_update

        ttk.Button(btn_frame, text="EKLE / ADD", style="Menu.TButton", command=cmd_add).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="GÜNCELLE / UPDATE", style="Menu.TButton", command=cmd_upd).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="SİL / DELETE", style="Menu.TButton", command=cmd_del).pack(side="left", padx=10)

    def add_personnel_form(self): self.user_form("Personel", "personel")
    def add_customer_form(self): self.user_form("Customer", "customer")

    def user_form(self, title, role):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=f"Yeni {title}", bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        self.app.create_form_entry(form_frame, "Ad Soyad:", "u_name", row=0)
        self.app.create_form_entry(form_frame, "Telefon:", "u_phone", row=1)
        self.app.create_form_entry(form_frame, "Kullanıcı Adı:", "u_user", row=2)
        self.app.create_form_entry(form_frame, "Şifre:", "u_pass", row=3)

        def save():
            if not self.app.u_user.get(): return
            
            if len(self.app.u_phone.get()) != 10:
                from tkinter import messagebox
                messagebox.showwarning("Error", self.app.t["error_phone"])
                return

            db = DataBase()
            db.add_user(self.app.u_user.get(), self.app.u_pass.get(), role, self.app.u_name.get(), self.app.u_phone.get())
            from tkinter import messagebox
            messagebox.showinfo("OK", "Eklendi!")
            if role == "personel": self.show_personnel()
            else: self.show_customers()

        ttk.Button(self.app.main_frame, text="KAYDET", style="Menu.TButton", command=save).pack(pady=20)

    def delete_personnel(self): self.delete_user_logic(self.show_personnel)
    def delete_customer(self): self.delete_user_logic(self.show_customers)

    def delete_user_logic(self, refresh_func):
        sel = self.app.user_tree.selection()
        if not sel: return
        uid = self.app.user_tree.item(sel)['values'][0]
        if uid == self.app.current_user[0]: 
            from tkinter import messagebox
            messagebox.showerror("Error", "Kendini silemezsin!")
            return
        
        DataBase().delete_user(uid)
        refresh_func()

    def open_personnel_update(self): self.open_update_form("Personel", "personel", self.show_personnel)
    def open_customer_update(self): self.open_update_form("Customer", "customer", self.show_customers)

    def open_update_form(self, title, role, refresh_func):
        sel = self.app.user_tree.selection()
        if not sel: return
        values = self.app.user_tree.item(sel)['values']
        user_id = values[0]

        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=f"{title} Güncelle", bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        self.app.create_form_entry(form_frame, "Ad Soyad:", "upt_u_name", row=0)
        self.app.upt_u_name.insert(0, values[1])
        self.app.create_form_entry(form_frame, "Kullanıcı Adı:", "upt_u_user", row=1)
        self.app.upt_u_user.insert(0, values[2])
        self.app.create_form_entry(form_frame, "Telefon:", "upt_u_phone", row=2)
        self.app.upt_u_phone.insert(0, values[3])
        self.app.create_form_entry(form_frame, "Şifre:", "upt_u_pass", row=3)
        self.app.upt_u_pass.insert(0, values[4])

        def save_update():
            if len(self.app.upt_u_phone.get()) != 10:
                from tkinter import messagebox
                messagebox.showwarning("Error", self.app.t["error_phone"])
                return
            
            db = DataBase()
            db.update_user(user_id, self.app.upt_u_name.get(), self.app.upt_u_user.get(), self.app.upt_u_phone.get(), self.app.upt_u_pass.get())
            from tkinter import messagebox
            messagebox.showinfo("OK", "Güncellendi")
            refresh_func()

        ttk.Button(self.app.main_frame, text="GÜNCELLE", style="Menu.TButton", command=save_update).pack(pady=20)