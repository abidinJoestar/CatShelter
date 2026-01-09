
TEXTS = {
    "TR": {
        # login page
        "window_title": "Kedi Barınağı Sistemi",
        "login_title": "Sisteme Giriş",
        "user_label": "Kullanıcı Adı:",
        "pass_label": "Şifre:",
        "personel_role": "Personel / Vet",
        "customer_role": "Sahiplenen",
        "login_btn_personel": "PERSONEL GİRİŞİ",
        "login_btn_customer": "MÜŞTERİ GİRİŞİ",
        "register_link": "Hesabınız yok mu? Kayıt Ol",
        "exit_btn": "Uygulamayı Kapat",
        
        # sign-in page
        "register_title": "Yeni Üyelik 🐾",
        "register_btn": "KAYDOL",
        "name_label": "Ad Soyad:",
        "phone_hint_label": "Telefon (5xxxxxxxxx):",
        
        "success_reg": "Kaydınız oluşturuldu! Giriş yapabilirsiniz.",
        "error_fill": "Lütfen tüm alanları doldurun.",
        "error_login": "Giriş bilgileri hatalı!",
        "error_phone": "Telefon numarası 10 haneli olmalı (Örn: 5xxxxxxxxx)",

        # main menu
        "menu_cat_manage": "Kedileri Yönet",
        "menu_cat_add": "Yeni Kedi Ekle",
        "menu_apps": "Başvurular",
        "menu_personnel": "Personel Listesi",
        "menu_customer": "Müşteri Listesi",
        "menu_reports": "Raporlar",
        "menu_cat_view": "Kedileri Gör",
        "menu_my_cats": "Sahiplendiklerim",
        "menu_about": "Hakkımızda",
        "menu_logout": "Çıkış Yap",
        "welcome": "Merhaba, {}!",
        "admin_panel": "Yönetici Paneli",
        "user_panel": "Sahiplenme Paneli",

        # cat form
        "title_new_cat": "Yeni Kedi Kaydı",
        "title_update_cat": "Kedi Güncelle",
        "lbl_cat_name": "Kedi Adı:",
        "lbl_cat_breed": "Türü:",
        "lbl_cat_age": "Yaşı:",
        "lbl_cat_gender": "Cinsiyet:",
        "lbl_cat_health": "Sağlık Durumu:",
        "lbl_cat_status": "Durumu:",

        "btn_health": "🏥 Sağlık Durumu",  # Bunu ekle
        "title_health": "Sağlık Notları",    # Bunu ekle
        "msg_no_health": "Bu kedi için girilmiş sağlık notu yok.",
        
        # combobox
        "combo_breeds": ["Tekir", "Van Kedisi", "British Shorthair", "Scottish Fold", "Siyam", "Sarman", "Sokak Kedisi", "Diğer"],
        "combo_ages": ["0-3 Aylık", "3-6 Aylık", "6-12 Aylık"] + [str(i) for i in range(1, 21)],
        "combo_genders": ["Dişi", "Erkek"],
        "combo_status": ["Barınakta", "Tedavide", "Sahiplendirildi"],

        # personel
        "header_personnel": "Personel Yönetimi",
        "header_customer": "Müşteri Yönetimi",
        "col_fullname": "Ad Soyad",
        "col_username": "Kullanıcı Adı",
        "col_phone": "Telefon",
        "col_pass": "Şifre",
        "col_cats": "Sahiplendiği Kediler",
        
        "title_new_personnel": "Yeni Personel Ekle",
        "title_new_customer": "Yeni Müşteri Ekle",
        "title_upt_personnel": "Personel Güncelle",
        "title_upt_customer": "Müşteri Güncelle",
        
        # buttons
        "btn_save": "KAYDET",
        "btn_cancel": "İPTAL",
        "btn_delete": "SİL",
        "btn_update": "GÜNCELLE",
        "btn_apply": "BAŞVURU YAP",
        "btn_add": "EKLE",
        "btn_add_personnel": "YENİ PERSONEL EKLE",
        "btn_add_customer": "YENİ MÜŞTERİ EKLE",
        
        # adoption
        "header_apps": "Bekleyen Başvurular",
        "header_my_cats": "Sahiplendiğim Dostlarım",
        "btn_approve": "ONAYLA ✅",
        "btn_reject": "REDDET ❌",
        
        # reports
        "menu_reports": "Raporlar",
        "header_reports": "İşlem Geçmişi / Loglar",
        "col_date": "Tarih & Saat",
        "col_action": "Yapılan İşlem",
        
        # reports detail
        "log_new_cat": "Yeni kedi eklendi: {} (Tür: {})",
        "log_delete_cat": "Kedi silindi: ID {}",
        "log_adopt": "Sahiplendirme yapıldı: {} -> {}",
        "log_login": "Kullanıcı giriş yaptı: {}",
        "log_clear": "Tüm kayıtlar temizlendi.",
        "log_new_cat": "Yeni kedi eklendi: {} (Tür: {})",
        "log_update": "Kedi bilgileri güncellendi: {}",
        "log_app_made": "Yeni sahiplendirme başvurusu: {}",
        "log_app_approved": "Başvuru onaylandı: {}",
        "log_app_rejected": "Başvuru reddedildi: {}",

        # messages
        "msg_added": "Başarıyla Eklendi!",
        "msg_updated": "Başarıyla Güncellendi!",
        "msg_app_sent": "Başvuru alındı.",
        "msg_wait": "Bu kedi şu an tedavide.",
        "msg_invalid": "Bu kedi uygun değil.",
        "msg_self_del": "Kendini silemezsin!",
        "msg_confirm_app": "{} isimli kedi için sahiplenme başvurusu yapmak istiyor musunuz?",

        # about
        "about_title": "Hakkında & Misyonumuz",
        "about_desc": "Bu Kedi Barınağı Yönetim Sistemi, sahipsiz dostlarımızı sıcak bir yuvayla buluşturmak ve barınak süreçlerini dijitalleştirmek amacıyla geliştirilmiştir.\n\nHer kedi, sevgi dolu bir evi hak eder. Teknolojiyi kullanarak onların hayatına dokunmayı hedefliyoruz.",
        "about_dev": "Geliştiriciler",
        "about_contact": "İletişim & Destek",
        "about_version": "Sürüm 1.0 - 2026",
        "about_uni": "Bahçeşehir Üniversitesi - Bilgisayar Mühendisliği"
    },
    "EN": {
        # login page
        "window_title": "Cat Shelter System",
        "login_title": "System Login",
        "user_label": "Username:",
        "pass_label": "Password:",
        "personel_role": "Staff / Vet",
        "customer_role": "Adopter",
        "login_btn_personel": "STAFF LOGIN",
        "login_btn_customer": "CUSTOMER LOGIN",
        "register_link": "No account? Sign Up",
        "exit_btn": "Close App",
        
        # sign-in page
        "register_title": "Join Us 🐾",
        "register_btn": "REGISTER",
        "name_label": "Full Name:",
        "phone_hint_label": "Phone (5xxxxxxxxx):",

        "success_reg": "Account created! You can login now.",
        "error_fill": "Please fill in all fields.",
        "error_login": "Invalid credentials!",
        "error_phone": "Phone must be 10 digits (Ex: 5xxxxxxxxx)",

        # main menu
        "menu_cat_manage": "Manage Cats",
        "menu_cat_add": "Add New Cat",
        "menu_apps": "Applications",
        "menu_personnel": "Staff List",
        "menu_customer": "Customer List",
        "menu_reports": "Reports",
        "menu_cat_view": "View Cats",
        "menu_my_cats": "My Adoptions",
        "menu_about": "About Us",
        "menu_logout": "Logout",
        "welcome": "Welcome, {}!",
        "admin_panel": "Admin Panel",
        "user_panel": "Adoption Panel",

        # reports
        "menu_reports": "Reports",
        "header_reports": "Action History / Logs",
        "col_date": "Date & Time",
        "col_action": "Action Detail",

        # reports detail
        "log_new_cat": "New cat added: {} (Breed: {})",
        "log_delete_cat": "Cat deleted: ID {}",
        "log_adopt": "Adoption approved: {} -> {}",
        "log_login": "User logged in: {}",
        "log_clear": "All logs cleared.",
        "log_new_cat": "New cat added: {} (Breed: {})",
        "log_update": "Cat details updated: {}",
        "log_app_made": "New adoption application: {}",
        "log_app_approved": "Application approved: {}",
        "log_app_rejected": "Application rejected: {}",
        
        # cat form
        "title_new_cat": "New Cat Registration",
        "title_update_cat": "Update Cat Info",
        "lbl_cat_name": "Name:",
        "lbl_cat_breed": "Breed:",
        "lbl_cat_age": "Age:",
        "lbl_cat_gender": "Gender:",
        "lbl_cat_health": "Health Status:",
        "lbl_cat_status": "Status:",

        "btn_health": "🏥 Health Status",
        "title_health": "Health Notes",
        "msg_no_health": "No health notes available for this cat.",
        
        # combobox
        "combo_breeds": ["Tabby", "Van Cat", "British Shorthair", "Scottish Fold", "Siamese", "Ginger", "Stray", "Other"],
        "combo_ages": ["0-3 Months", "3-6 Months", "6-12 Months"] + [str(i) for i in range(1, 21)],
        "combo_genders": ["Female", "Male"],
        "combo_status": ["In Shelter", "Under Treatment", "Adopted"],

        # personel
        "header_personnel": "Staff Management",
        "header_customer": "Customer Management",
        "col_fullname": "Full Name",
        "col_username": "Username",
        "col_phone": "Phone",
        "col_pass": "Password",
        "col_cats": "Adopted Cats",
        
        "title_new_personnel": "Add New Staff",
        "title_new_customer": "Add New Customer",
        "title_upt_personnel": "Update Staff",
        "title_upt_customer": "Update Customer",

        # button
        "btn_save": "SAVE",
        "btn_cancel": "CANCEL",
        "btn_delete": "DELETE",
        "btn_update": "UPDATE",
        "btn_apply": "APPLY",
        "btn_add": "ADD",
        "btn_add_personnel": "ADD NEW STAFF",
        "btn_add_customer": "ADD NEW CUSTOMER",

        # adoption
        "header_apps": "Pending Applications",
        "header_my_cats": "My Adopted Friends",
        "btn_approve": "APPROVE ✅",
        "btn_reject": "REJECT ❌",

        # message
        "msg_added": "Successfully Added!",
        "msg_updated": "Successfully Updated!",
        "msg_app_sent": "Application sent.",
        "msg_wait": "This cat is currently under treatment.",
        "msg_invalid": "This cat is not available.",
        "msg_self_del": "You cannot delete yourself!",
        "msg_confirm_app": "Do you want to apply to adopt {}?",

        # about
        "about_title": "About & Mission",
        "about_desc": "This Cat Shelter Management System is developed to connect homeless cats with loving homes and digitize shelter processes.\n\nEvery cat deserves a loving home. We aim to touch their lives using technology.",
        "about_dev": "Developers",
        "about_contact": "Contact & Support",
        "about_version": "Version 1.0 - 2026",
        "about_uni": "Bahcesehir University - Computer Engineering"
    
    }
}

# database mapping
DB_MAPPING = {
    # tr
    "Barınakta": "Barınakta",
    "Tedavide": "Tedavide",
    "Sahiplendirildi": "Sahiplendirildi",
    "Tekir": "Tekir",
    "Dişi": "Dişi",
    "Erkek": "Erkek",
    # eng
    "In Shelter": "Barınakta",
    "Under Treatment": "Tedavide",
    "Adopted": "Sahiplendirildi",
    "Tabby": "Tekir",
    "Female": "Dişi",
    "Male": "Erkek",
    "Van Cat": "Van Kedisi",
    "Stray": "Sokak Kedisi",
    "Ginger": "Sarman",
    "Other": "Diğer",
    "British Shorthair": "British Shorthair", # Ortak
    "Scottish Fold": "Scottish Fold",         # Ortak
    "Siamese": "Siyam",
    "Siyam": "Siyam"
}

def get_display_text(db_value, lang_code):
    if lang_code == "TR": return db_value     
    reverse_map = {
        "Barınakta": "In Shelter",
        "Tedavide": "Under Treatment",
        "Sahiplendirildi": "Adopted",
        "Tekir": "Tabby",
        "Dişi": "Female",
        "Erkek": "Male",
        "Van Kedisi": "Van Cat",
        "Sokak Kedisi": "Stray",
        "Sarman": "Ginger",
        "Diğer": "Other",
        "Siyam": "Siamese"
    }
    return reverse_map.get(db_value, db_value)