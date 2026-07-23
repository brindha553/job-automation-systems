import sqlite3
import os
from app import create_app
from extensions import db

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'talentmatch.db')
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        columns_to_add = [
            "parsed_description TEXT",
            "preferred_skills VARCHAR(255)",
            "technologies VARCHAR(500)",
            "education VARCHAR(150)",
            "minimum_experience INTEGER",
            "maximum_experience INTEGER",
            "salary_min INTEGER",
            "salary_max INTEGER",
            "work_mode VARCHAR(50)",
            "industry VARCHAR(150)",
            "keywords VARCHAR(500)",
            "ai_summary TEXT",
            "ai_domain VARCHAR(100)",
            "classification_confidence FLOAT",
            "processed BOOLEAN DEFAULT 0",
            "processed_at DATETIME"
        ]
        
        for col in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE jobs ADD COLUMN {col}")
                print(f"Added column {col.split(' ')[0]}")
            except sqlite3.OperationalError as e:
                print(f"Skipped {col.split(' ')[0]}: {e}")
                
        conn.commit()
        conn.close()
        print("Phase 4 Migration finished.")
    else:
        print("Database not found, no migration needed.")

if __name__ == '__main__':
    migrate()
