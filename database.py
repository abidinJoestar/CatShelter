import sqlite3
import datetime

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
            cur.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cat_id INTEGER,
                    user_id INTEGER,
                    status TEXT DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT (datetime('now','localtime'))
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_text TEXT,
                    created_at TIMESTAMP DEFAULT (datetime('now','localtime'))
                )
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

    # user actions
    def check_login(self, username, password, role):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
            return cur.fetchone()

    def add_user(self, username, password, role, fullname, phone, lang=None):
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO users (username, password, role, fullname, phone) VALUES (?, ?, ?, ?, ?)",
                            (username, password, role, fullname, phone))
                
                log_data = f"log_new_user|||{role}|||{fullname}|||{username}"
                # Burada artık doğru tablo ismini kullanıyoruz: action_text
                cur.execute("INSERT INTO logs (action_text) VALUES (?)", (log_data,))
                
                conn.commit()
                return True, "Success"
        except sqlite3.IntegrityError:
             return False, "Username exists"

    def get_all_personnel(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, fullname, username, phone, password FROM users WHERE role='personel'")
            return cur.fetchall()

    def delete_user(self, user_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()

    def update_user(self, user_id, fullname, username, phone, password):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE users 
                SET fullname=?, username=?, phone=?, password=?
                WHERE id=?
            """, (fullname, username, phone, password, user_id))
            conn.commit()

    # cat actions
    def add_cat(self, name, breed, age, gender, status, health, image_path, lang=None):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO cats (name, breed, age, gender, status, health_notes, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (name, breed, age, gender, status, health, image_path))
            
            log_data = f"log_new_cat|||{name}|||{breed}"
            cur.execute("INSERT INTO logs (action_text) VALUES (?)", (log_data,))
            
            conn.commit()

    def get_all_cats(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, breed, age, gender, status FROM cats")
            return cur.fetchall()
        
    def get_cat_health(self, cat_id):
        """Sadece seçilen kedinin sağlık notunu getirir"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            res = cur.execute("SELECT health_notes FROM cats WHERE id=?", (cat_id,)).fetchone()
            return res[0] if res else ""

    def delete_cat(self, cat_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            # Önce kediyi sil
            cur.execute("DELETE FROM cats WHERE id=?", (cat_id,))
            conn.commit()

    def update_cat(self, cat_id, name, breed, age, gender, status, health_notes):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE cats 
                SET name=?, breed=?, age=?, gender=?, status=?, health_notes=?
                WHERE id=?
            """, (name, breed, age, gender, status, health_notes, cat_id))
            conn.commit()

    # adoption
    def apply_adoption(self, cat_id, user_id, lang=None):
        with self.get_connection() as conn:
            cur = conn.cursor()
            check = cur.execute("SELECT * FROM applications WHERE cat_id=? AND user_id=?", (cat_id, user_id)).fetchone()
            if check: return 
            
            cur.execute("INSERT INTO applications (cat_id, user_id) VALUES (?, ?)", (cat_id, user_id))
            
            cat_name_row = cur.execute("SELECT name FROM cats WHERE id=?", (cat_id,)).fetchone()
            cat_name = cat_name_row[0] if cat_name_row else "?"
            
            log_data = f"log_app_made|||{cat_name}"
            cur.execute("INSERT INTO logs (action_text) VALUES (?)", (log_data,))
            
            conn.commit()

    def get_pending_applications(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            query = """
                SELECT a.cat_id, c.name, c.breed, u.fullname, u.phone 
                FROM applications a
                JOIN cats c ON a.cat_id = c.id
                JOIN users u ON a.user_id = u.id
            """
            cur.execute(query)
            return cur.fetchall()

    def process_application(self, cat_id, decision, lang=None):
        with self.get_connection() as conn:
            cur = conn.cursor()
            app_info = cur.execute("SELECT user_id FROM applications WHERE cat_id=?", (cat_id,)).fetchone()
            
            cat_name_row = cur.execute("SELECT name FROM cats WHERE id=?", (cat_id,)).fetchone()
            cat_name = cat_name_row[0] if cat_name_row else f"ID:{cat_id}"

            if decision == 'approve':
                cur.execute("UPDATE cats SET status='Sahiplendirildi' WHERE id=?", (cat_id,))
                if app_info:
                    cur.execute("UPDATE cats SET owner_id=? WHERE id=?", (app_info[0], cat_id))
                cur.execute("DELETE FROM applications WHERE cat_id=?", (cat_id,))
                                
            else: # reject
                cur.execute("DELETE FROM applications WHERE cat_id=?", (cat_id,))
                            
            conn.commit()

    def get_user_cats(self, user_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, name, breed, age, gender, status FROM cats WHERE owner_id=? AND status='Sahiplendirildi'", (user_id,))
            return cur.fetchall()

    def get_all_customers(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
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
    
    # report actions
    def add_log(self, action_text):
        """
        Log ekler. 'created_at' otomatik eklenir.
        """
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO logs (action_text) VALUES (?)", (action_text,))
            conn.commit()

    def get_all_logs(self):
        """Tüm logları tarihe göre (yeni en üstte) getirir"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT created_at, action_text FROM logs ORDER BY id DESC")
            return cur.fetchall()

    def clear_all_logs(self):
        """Tüm logları siler"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM logs")
            conn.commit()