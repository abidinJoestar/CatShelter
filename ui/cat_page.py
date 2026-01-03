import tkinter as tk
from tkinter import ttk
import sys
sys.path.append("..") 
from database import DataBase 

class CatPage:
    def __init__(self, app):
        self.app = app # Main Window'a erişim sağlar

    def show_cats(self):
        self.app.clear_main_frame()
        baslik = "Kedi Yönetim Listesi" if self.app.current_user[3] == 'personel' else "Sahiplenilmeyi Bekleyen Dostlarımız"
        tk.Label(self.app.main_frame, text=baslik, bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)

        table_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "name", "breed", "age", "gender", "status")
        self.app.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
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

        if self.app.current_user[3] == 'personel':
            ttk.Button(btn_frame, text="Seçili Kediyi Sil", style="Menu.TButton", command=self.delete_selected_cat).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="Bilgileri Güncelle", style="Menu.TButton", command=self.open_update_form).pack(side="left", padx=5)
        else:
            # Başvuru işlemleri AdoptionPage'de ama butonu burada
            from ui.adoption_page import AdoptionPage
            adoption_logic = AdoptionPage(self.app)
            ttk.Button(btn_frame, text="BAŞVURU YAP", style="Menu.TButton", command=adoption_logic.apply_for_cat).pack(side="left", padx=5)

    def add_cat(self):
        self.app.clear_main_frame()
        tk.Label(self.app.main_frame, text="Yeni Kedi Kaydı", bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        self.app.create_form_entry(form_frame, "Kedi Adı:", "name_entry", row=0)
        
        tk.Label(form_frame, text="Türü:", bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.breed_combo = ttk.Combobox(form_frame, values=["Tekir", "Van Kedisi", "British Shorthair", "Scottish Fold", "Siyam", "Sarman", "Sokak Kedisi", "Diğer"], width=28, state="readonly")
        self.breed_combo.grid(row=1, column=1, pady=10, sticky="w")
        self.breed_combo.current(0) 

        tk.Label(form_frame, text="Yaşı:", bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        yas_listesi = ["0-3 Aylık", "3-6 Aylık", "6-12 Aylık"] + [str(i) for i in range(1, 21)]
        self.age_combo = ttk.Combobox(form_frame, values=yas_listesi, width=28, state="readonly")
        self.age_combo.grid(row=2, column=1, pady=10, sticky="w")
        self.age_combo.current(0) 

        tk.Label(form_frame, text="Cinsiyet:", bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", pady=10, padx=10)
        self.gender_combo = ttk.Combobox(form_frame, values=["Dişi", "Erkek"], width=28, state="readonly")
        self.gender_combo.grid(row=3, column=1, pady=10, sticky="w")
        self.gender_combo.current(0)

        self.app.create_form_entry(form_frame, "Sağlık Durumu:", "health_entry", row=4)
        ttk.Button(self.app.main_frame, text="KEDİYİ KAYDET", style="Menu.TButton", command=self.save_new_cat).pack(pady=30, ipadx=20, ipady=5)

    def save_new_cat(self):
        name = self.app.name_entry.get()
        if not name: return
        try:
            db = DataBase()
            db.add_cat(name, self.breed_combo.get(), self.age_combo.get(), self.gender_combo.get(), "Barınakta", self.app.health_entry.get(), "")
            from tkinter import messagebox
            messagebox.showinfo("Başarılı", "Eklendi!")
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
        tk.Label(self.app.main_frame, text="Kedi Bilgilerini Güncelle", bg=self.app.main_bg, fg="#004f63", font=("Segoe UI", 24, "bold")).pack(pady=20)
        
        form_frame = tk.Frame(self.app.main_frame, bg=self.app.main_bg)
        form_frame.pack(pady=10)

        self.app.create_form_entry(form_frame, "Kedi Adı:", "upt_name", row=0)
        self.app.upt_name.insert(0, values[1])

        # Comboboxlar...
        tk.Label(form_frame, text="Türü:", bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=1, column=0, sticky="e", pady=10, padx=10)
        self.upt_breed = ttk.Combobox(form_frame, values=["Tekir", "Van Kedisi", "British Shorthair", "Scottish Fold", "Siyam", "Sarman", "Sokak Kedisi", "Diğer"], width=28, state="readonly")
        self.upt_breed.grid(row=1, column=1, pady=10, sticky="w")
        self.upt_breed.set(values[2]) 

        tk.Label(form_frame, text="Yaşı:", bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        yas_listesi = ["0-3 Aylık", "3-6 Aylık", "6-12 Aylık"] + [str(i) for i in range(1, 21)]
        self.upt_age = ttk.Combobox(form_frame, values=yas_listesi, width=28, state="readonly")
        self.upt_age.grid(row=2, column=1, pady=10, sticky="w")
        self.upt_age.set(values[3])

        tk.Label(form_frame, text="Cinsiyet:", bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=3, column=0, sticky="e", pady=10, padx=10)
        self.upt_gender = ttk.Combobox(form_frame, values=["Dişi", "Erkek"], width=28, state="readonly")
        self.upt_gender.grid(row=3, column=1, pady=10, sticky="w")
        self.upt_gender.set(values[4]) 

        tk.Label(form_frame, text="Durumu:", bg=self.app.main_bg, font=("Segoe UI", 12)).grid(row=4, column=0, sticky="e", pady=10, padx=10)
        self.upt_status = ttk.Combobox(form_frame, values=["Barınakta", "Tedavide", "Sahiplendirildi"], width=28, state="readonly")
        self.upt_status.grid(row=4, column=1, pady=10, sticky="w")
        self.upt_status.set(values[5]) 

        self.app.create_form_entry(form_frame, "Sağlık Notu:", "upt_health", row=5)
        ttk.Button(self.app.main_frame, text="KAYDET", style="Menu.TButton", command=self.save_update).pack(pady=20)
        ttk.Button(self.app.main_frame, text="İptal", command=self.show_cats).pack()

    def save_update(self):
        try:
            db = DataBase()
            db.update_cat(self.selected_cat_id, self.app.upt_name.get(), self.upt_breed.get(), self.upt_age.get(), self.upt_gender.get(), self.upt_status.get(), self.app.upt_health.get())
            from tkinter import messagebox
            messagebox.showinfo("Başarılı", "Güncellendi!")
            self.show_cats()
        except Exception as e:
            pass