import tkinter as tk
from tkinter import ttk
import sys
sys.path.append("..") 
from database import DataBase 

class CatPage:
    def __init__(self, app):
        self.app = app # MainApp örneğine erişim

    def show_cats(self):
        self.app.clear_main_frame()
        # Başlığı dilden çek
        baslik = self.app.t["menu_cat_manage"] if self.app.current_user[3] == 'personel' else self.app.t["menu_cat_view"]
        
        tk.Label(self.app.main_frame, text=baslik, bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)

        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "name", "breed", "age", "gender", "status")
        self.app.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Sütun başlıklarını da (opsiyonel) sözlükten çekebiliriz ama şimdilik capitalize yeterli
        for col in columns: self.app.tree.heading(col, text=col.capitalize())
        self.app.tree.column("id", width=30, anchor="center")
        self.app.tree.column("age", width=50, anchor="center")
        self.app.tree.column("gender", width=70)
        
        self.app.tree.pack(fill="both", expand=True)

        try:
            db = DataBase()
            cats = db.get_all_cats()
            for cat in cats:
                self.app.tree.insert("", tk.END, values=cat)
        except Exception as e:
            tk.Label(self.app.main_frame, text=f"Hata: {e}").pack()

        btn_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        btn_frame.pack(pady=10)

        # BUTONLARIN DİLİNİ AYARLADIK
        if self.app.current_user[3] == 'personel':
            ttk.Button(btn_frame, text=self.app.t["btn_delete"], style="Menu.TButton", command=self.delete_selected_cat).pack(side="left", padx=5)
            ttk.Button(btn_frame, text=self.app.t["btn_update"], style="Menu.TButton", command=self.open_update_form).pack(side="left", padx=5)
        else:
            # Başvuru için AdoptionPage'e eriş
            ttk.Button(btn_frame, text=self.app.t["btn_apply"], style="Menu.TButton", command=self.app.adoption_page.apply_for_cat).pack(side="left", padx=5)

    def add_cat(self):
        self.app.clear_main_frame()
        # BAŞLIK DÜZELDİ
        tk.Label(self.app.main_frame, text=self.app.t["title_new_cat"], bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        # ETİKETLER DÜZELDİ
        self.app.create_form_entry(form_frame, self.app.t["lbl_cat_name"], "name_entry", row=0)
        
        tk.Label(form_frame, text=self.app.t["lbl_cat_breed"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.breed_combo = ttk.Combobox(form_frame, values=["Tekir", "Van Kedisi", "British Shorthair", "Scottish Fold", "Siyam", "Sarman", "Sokak Kedisi", "Diğer"], width=28, state="readonly")
        self.breed_combo.grid(row=1, column=1, pady=10, sticky="w")
        self.breed_combo.current(0) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_age"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        yas_listesi = ["0-3 Aylık", "3-6 Aylık", "6-12 Aylık"] + [str(i) for i in range(1, 21)]
        self.age_combo = ttk.Combobox(form_frame, values=yas_listesi, width=28, state="readonly")
        self.age_combo.grid(row=2, column=1, pady=10, sticky="w")
        self.age_combo.current(0) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_gender"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", pady=10, padx=10)
        self.gender_combo = ttk.Combobox(form_frame, values=["Dişi", "Erkek"], width=28, state="readonly")
        self.gender_combo.grid(row=3, column=1, pady=10, sticky="w")
        self.gender_combo.current(0)

        self.app.create_form_entry(form_frame, self.app.t["lbl_cat_health"], "health_entry", row=4)
        
        # BUTON DÜZELDİ
        ttk.Button(self.app.main_frame, text=self.app.t["btn_save"], style="Menu.TButton", command=self.save_new_cat).pack(pady=30, ipadx=20, ipady=5)

    def save_new_cat(self):
        name = self.app.name_entry.get()
        if not name: return
        try:
            db = DataBase()
            db.add_cat(name, self.breed_combo.get(), self.age_combo.get(), self.gender_combo.get(), "Barınakta", self.app.health_entry.get(), "")
            from tkinter import messagebox
            messagebox.showinfo("OK", self.app.t["msg_added"])
            self.show_cats() 
        except Exception as e:
            pass

    def delete_selected_cat(self):
        selected = self.app.tree.selection()
        if selected:
            cat_id = self.app.tree.item(selected)['values'][0]
            DataBase().delete_cat(cat_id)
            self.show_cats()

    def open_update_form(self):
        selected = self.app.tree.selection()
        if not selected: return

        values = self.app.tree.item(selected)['values']
        self.selected_cat_id = values[0] 
        
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text=self.app.t["title_update_cat"], bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        # GÜNCELLEME ETİKETLERİ DÜZELDİ
        self.app.create_form_entry(form_frame, self.app.t["lbl_cat_name"], "upt_name", row=0)
        self.app.upt_name.insert(0, values[1])

        tk.Label(form_frame, text=self.app.t["lbl_cat_breed"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.upt_breed = ttk.Combobox(form_frame, values=["Tekir", "Van Kedisi", "British Shorthair", "Scottish Fold", "Siyam", "Sarman", "Sokak Kedisi", "Diğer"], width=28, state="readonly")
        self.upt_breed.grid(row=1, column=1, pady=10, sticky="w")
        self.upt_breed.set(values[2]) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_age"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        yas_listesi = ["0-3 Aylık", "3-6 Aylık", "6-12 Aylık"] + [str(i) for i in range(1, 21)]
        self.upt_age = ttk.Combobox(form_frame, values=yas_listesi, width=28, state="readonly")
        self.upt_age.grid(row=2, column=1, pady=10, sticky="w")
        self.upt_age.set(values[3])

        tk.Label(form_frame, text=self.app.t["lbl_cat_gender"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", pady=10, padx=10)
        self.upt_gender = ttk.Combobox(form_frame, values=["Dişi", "Erkek"], width=28, state="readonly")
        self.upt_gender.grid(row=3, column=1, pady=10, sticky="w")
        self.upt_gender.set(values[4]) 

        tk.Label(form_frame, text=self.app.t["lbl_cat_status"], bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=4, column=0, sticky="e", pady=10, padx=10)
        self.upt_status = ttk.Combobox(form_frame, values=["Barınakta", "Tedavide", "Sahiplendirildi"], width=28, state="readonly")
        self.upt_status.grid(row=4, column=1, pady=10, sticky="w")
        self.upt_status.set(values[5]) 

        self.app.create_form_entry(form_frame, self.app.t["lbl_cat_health"], "upt_health", row=5)
        
        # BUTONLAR DÜZELDİ
        ttk.Button(self.app.main_frame, text=self.app.t["btn_save"], style="Menu.TButton", command=self.save_update).pack(pady=20)
        ttk.Button(self.app.main_frame, text=self.app.t["btn_cancel"], command=self.show_cats).pack()

    def save_update(self):
        try:
            db = DataBase()
            db.update_cat(self.selected_cat_id, self.app.upt_name.get(), self.upt_breed.get(), self.upt_age.get(), self.upt_gender.get(), self.upt_status.get(), self.app.upt_health.get())
            from tkinter import messagebox
            messagebox.showinfo("OK", self.app.t["msg_updated"])
            self.show_cats()
        except Exception as e:
            pass