import sqlite3

class DataBase:
    def __init__(self, db_name="catshelter.db"):
        self.db_name = db_name
        self.create_table()
        self.fill_test_data()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            # users
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT,
                    fullname TEXT,
                    phone TEXT
                );
            """)
            # cats
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    breed TEXT,
                    age TEXT,
                    gender TEXT,
                    status TEXT DEFAULT 'Barınakta',
                    health_notes TEXT,
                    image_path TEXT,
                    owner_id INTEGER
                );
            """)

    def fill_test_data(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users")
            if cur.fetchone()[0] == 0:
                print("Test kullanıcıları yükleniyor...")
                users_data = [
                    ('admin', '1234', 'personel', 'Sistem Yöneticisi', '555-0001'),
                    ('ufuk', '1234', 'personel', 'Ufuk Karacali', '555-0002'),
                    ('musteri1', '1234', 'customer', 'Burak Ege Kaya', '555-9999')
                ]
                cur.executemany("INSERT INTO users(username, password, role, fullname, phone) VALUES(?, ?, ?, ?, ?)", users_data)
            
            cur.execute("SELECT COUNT(*) FROM cats")
            if cur.fetchone()[0] == 0:
                print("Test kedileri yükleniyor...")
                cats_data = [
                    ('Pamuk', 'Van Kedisi', '2', 'Dişi', 'Barınakta', 'Sağlıklı', '', None),
                    ('Duman', 'British Shorthair', '1', 'Erkek', 'Barınakta', 'Aşıları tam', '', None),
                    ('Tekir', 'Sokak Kedisi', '4', 'Dişi', 'Tedavide', 'Ayağı kırık', '', None)
                ]
                cur.executemany("INSERT INTO cats(name, breed, age, gender, status, health_notes, image_path, owner_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", cats_data)
            conn.commit()

    # --- KULLANICI İŞLEMLERİ ---
    def check_login(self, username, password, role):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
            return cur.fetchone()

    def add_user(self, username, password, role, fullname, phone):
        """Yeni bir kullanıcı (Personel veya Müşteri) ekler"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO users (username, password, role, fullname, phone)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, password, role, fullname, phone))
                conn.commit()
                return True, "Kayıt Başarılı"
            except sqlite3.IntegrityError:
                return False, "Bu kullanıcı adı zaten kullanılıyor."
            except Exception as e:
                return False, f"Hata: {e}"
            
            # --- PERSONEL YÖNETİMİ (LİSTELEME, SİLME, GÜNCELLEME) ---
   
    def get_all_personnel(self):
        """Sadece personelleri listeler"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, fullname, username, phone, password FROM users WHERE role='personel'")
            return cur.fetchall()

    def delete_user(self, user_id):
        """Kullanıcıyı siler"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()

    def update_user(self, user_id, fullname, username, phone, password):
        """Kullanıcı bilgilerini günceller"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE users 
                SET fullname=?, username=?, phone=?, password=?
                WHERE id=?
            """, (fullname, username, phone, password, user_id))
            conn.commit()

    # --- KEDİ YÖNETİMİ ---
    def add_cat(self, name, breed, age, gender, status, health_notes, image_path):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO cats (name, breed, age, gender, status, health_notes, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, breed, age, gender, status, health_notes, image_path))
            conn.commit()

    def get_all_cats(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, breed, age, gender, status FROM cats")
            return cur.fetchall()

    def delete_cat(self, cat_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM cats WHERE id=?", (cat_id,))
            conn.commit()

    # --- BAŞVURU SİSTEMİ (YENİLENEN KISIM) ---
    
    def apply_adoption(self, cat_id, user_id):
        """Müşteri başvuru yapınca çalışır. Durumu 'Başvuru Bekliyor' yapar."""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE cats SET status=?, owner_id=? WHERE id=?", 
                        ('Başvuru Bekliyor', user_id, cat_id))
            conn.commit()

    def get_pending_applications(self):
        """Personel için bekleyen başvuruları ve başvuranın adını getirir"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            # Kedi bilgileriyle Kullanıcı bilgilerini birleştiriyoruz (JOIN)
            query = """
                SELECT c.id, c.name, c.breed, u.fullname, u.phone 
                FROM cats c 
                JOIN users u ON c.owner_id = u.id 
                WHERE c.status = 'Başvuru Bekliyor'
            """
            cur.execute(query)
            return cur.fetchall()

    def process_application(self, cat_id, decision):
        """Başvuruyu onaylar veya reddeder"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            if decision == "approve":
                # Onaylanırsa durum 'Sahiplendirildi' olur
                cur.execute("UPDATE cats SET status='Sahiplendirildi' WHERE id=?", (cat_id,))
            else:
                # Reddedilirse kedi boşa çıkar ('Barınakta'), sahibi silinir
                cur.execute("UPDATE cats SET status='Barınakta', owner_id=NULL WHERE id=?", (cat_id,))
            conn.commit()

    def update_cat(self, cat_id, name, breed, age, gender, status, health_notes):
        """Kedinin bilgilerini günceller"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE cats 
                SET name=?, breed=?, age=?, gender=?, status=?, health_notes=?
                WHERE id=?
            """, (name, breed, age, gender, status, health_notes, cat_id))
            conn.commit()
            
    def get_user_cats(self, user_id):
        """Müşterinin SADECE ONAYLANMIŞ kedilerini getirir"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, breed, age, gender, status FROM cats WHERE owner_id=? AND status='Sahiplendirildi'", (user_id,))
            return cur.fetchall()
        
    def get_all_customers(self):
        """Müşterileri ve sahiplendikleri (Onaylanmış) kedileri listeler"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            # LEFT JOIN ile kedi isimlerini alıp virgülle birleştiriyoruz.
            # Sadece durumu 'Sahiplendirildi' olanları çekiyoruz.
            query = """
                SELECT u.id, u.fullname, u.username, u.phone, u.password, 
                       GROUP_CONCAT(c.name, ', ') 
                FROM users u 
                LEFT JOIN cats c ON u.id = c.owner_id AND c.status='Sahiplendirildi'
                WHERE u.role='customer' 
                GROUP BY u.id
            """
            cur.execute(query)
            return cur.fetchall()