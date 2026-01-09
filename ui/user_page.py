import tkinter as tk
from tkinter import ttk
import sys
sys.path.append("..") 
from database import DataBase 

class UserPage:
    def __init__(self, app):
        self.app = app

    def show_personnel(self):
        # Başlık ve Veri
        self.show_user_list(self.app.t["header_personnel"], DataBase().get_all_personnel(), is_customer=False)

    def show_customers(self):
        # Başlık ve Veri
        self.show_user_list(self.app.t["header_customer"], DataBase().get_all_customers(), is_customer=True)

    def show_user_list(self, title_text, data, is_customer=False):
        self.app.clear_main_frame()
        # Dinamik Başlık
        tk.Label(self.app.main_frame, text=title_text, bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)

        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sütun ID'leri (Kod içinde kullanmak için İngilizce kalabilir, kullanıcıya görünen kısmı değiştireceğiz)
        columns = ["id", "fullname", "username", "phone", "password"]
        if is_customer: columns.append("cats")

        self.app.user_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.app.user_tree.pack(fill="both", expand=True)

        # --- DİNAMİK SÜTUN BAŞLIKLARI ---
        # id sütunu gizli veya küçük olabilir, diğerlerini sözlükten çekiyoruz
        self.app.user_tree.heading("id", text="ID") 
        self.app.user_tree.heading("fullname", text=self.app.t["col_fullname"])
        self.app.user_tree.heading("username", text=self.app.t["col_username"])
        self.app.user_tree.heading("phone", text=self.app.t["col_phone"])
        self.app.user_tree.heading("password", text=self.app.t["col_pass"])
        
        if is_customer:
            self.app.user_tree.heading("cats", text=self.app.t["col_cats"])

        # Veri doldurma
        if data:
            for item in data:
                if is_customer:
                    l = list(item)
                    if len(l) > 5 and l[5] is None: l[5] = "-"
                    self.app.user_tree.insert("", tk.END, values=l)
                else:
                    self.app.user_tree.insert("", tk.END, values=item)

        # BUTONLAR
        btn_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        btn_frame.pack(pady=10)
        
        if is_customer:
            btn_add_text = self.app.t["btn_add_customer"]
            cmd_add = self.add_customer_form
            cmd_upd = self.open_customer_update
            cmd_del = self.delete_customer
        else:
            btn_add_text = self.app.t["btn_add_personnel"]
            cmd_add = self.add_personnel_form
            cmd_upd = self.open_personnel_update
            cmd_del = self.delete_personnel

        ttk.Button(btn_frame, text=btn_add_text, style="Menu.TButton", command=cmd_add).pack(side="left", padx=10)
        ttk.Button(btn_frame, text=self.app.t["btn_update"], style="Menu.TButton", command=cmd_upd).pack(side="left", padx=10)
        ttk.Button(btn_frame, text=self.app.t["btn_delete"], style="Menu.TButton", command=cmd_del).pack(side="left", padx=10)

    # --- EKLEME FORMLARI ---
    def add_personnel_form(self): 
        self.user_form(self.app.t["title_new_personnel"], "personel")
    
    def add_customer_form(self): 
        self.user_form(self.app.t["title_new_customer"], "customer")

    def user_form(self, title_text, role):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=title_text, bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        self.app.create_form_entry(form_frame, self.app.t["col_fullname"] + ":", "u_name", row=0)
        self.app.create_form_entry(form_frame, self.app.t["col_phone"] + ":", "u_phone", row=1)
        self.app.create_form_entry(form_frame, self.app.t["col_username"] + ":", "u_user", row=2)
        self.app.create_form_entry(form_frame, self.app.t["col_pass"] + ":", "u_pass", row=3)

        def save():
            if not self.app.u_user.get(): return
            
            if len(self.app.u_phone.get()) != 10:
                from tkinter import messagebox
                messagebox.showwarning("Error", self.app.t["error_phone"])
                return

            db = DataBase()
            db.add_user(self.app.u_user.get(), self.app.u_pass.get(), role, self.app.u_name.get(), self.app.u_phone.get(), lang=self.app.lang)
            from tkinter import messagebox
            messagebox.showinfo("OK", self.app.t["msg_added"])
            if role == "personel": self.show_personnel()
            else: self.show_customers()

        ttk.Button(self.app.main_frame, text=self.app.t["btn_save"], style="Menu.TButton", command=save).pack(pady=20)
        cancel_cmd = self.show_personnel if role == "personel" else self.show_customers
        ttk.Button(self.app.main_frame, text=self.app.t["btn_cancel"], command=cancel_cmd).pack()

    # delete
    def delete_personnel(self): self.delete_user_logic(self.show_personnel)
    def delete_customer(self): self.delete_user_logic(self.show_customers)

    def delete_user_logic(self, refresh_func):
        sel = self.app.user_tree.selection()
        if not sel: return
        uid = self.app.user_tree.item(sel)['values'][0]
        if uid == self.app.current_user[0]: 
            from tkinter import messagebox
            messagebox.showerror("Error", self.app.t["msg_self_del"])
            return
        
        DataBase().delete_user(uid)
        refresh_func()

    # update
    def open_personnel_update(self): 
        self.open_update_form(self.app.t["title_upt_personnel"], "personel", self.show_personnel)
    
    def open_customer_update(self): 
        self.open_update_form(self.app.t["title_upt_customer"], "customer", self.show_customers)

    def open_update_form(self, title_text, role, refresh_func):
        sel = self.app.user_tree.selection()
        if not sel: return
        values = self.app.user_tree.item(sel)['values']
        user_id = values[0]

        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=title_text, bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        self.app.create_form_entry(form_frame, self.app.t["col_fullname"] + ":", "upt_u_name", row=0)
        self.app.upt_u_name.insert(0, values[1])
        
        self.app.create_form_entry(form_frame, self.app.t["col_username"] + ":", "upt_u_user", row=1)
        self.app.upt_u_user.insert(0, values[2])
        
        self.app.create_form_entry(form_frame, self.app.t["col_phone"] + ":", "upt_u_phone", row=2)
        self.app.upt_u_phone.insert(0, values[3])
        
        self.app.create_form_entry(form_frame, self.app.t["col_pass"] + ":", "upt_u_pass", row=3)
        self.app.upt_u_pass.insert(0, values[4])

        def save_update():
            if len(self.app.upt_u_phone.get()) != 10:
                from tkinter import messagebox
                messagebox.showwarning("Error", self.app.t["error_phone"])
                return
            
            db = DataBase()
            db.update_user(user_id, self.app.upt_u_name.get(), self.app.upt_u_user.get(), self.app.upt_u_phone.get(), self.app.upt_u_pass.get())
            from tkinter import messagebox
            messagebox.showinfo("OK", self.app.t["msg_updated"])
            refresh_func()

        ttk.Button(self.app.main_frame, text=self.app.t["btn_update"], style="Menu.TButton", command=save_update).pack(pady=20)
        ttk.Button(self.app.main_frame, text=self.app.t["btn_cancel"], command=refresh_func).pack()