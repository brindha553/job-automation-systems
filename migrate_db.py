import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database', 'talentmatch.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    columns_to_add = [
        "full_name VARCHAR(120)",
        "phone VARCHAR(20)",
        "college VARCHAR(150)",
        "department VARCHAR(150)",
        "academic_year VARCHAR(50)",
        "profile_image VARCHAR(255) DEFAULT 'default.jpg'",
        "updated_at DATETIME"
    ]
    
    for col in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col}")
            print(f"Added column {col.split(' ')[0]}")
        except sqlite3.OperationalError as e:
            print(f"Skipped {col.split(' ')[0]}: {e}")
            
    conn.commit()
    conn.close()
    print("Migration finished.")
else:
    print("Database not found, no migration needed.")
