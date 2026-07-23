import sqlite3
import os
from app import create_app
from extensions import db

def migrate():
    app = create_app()
    with app.app_context():
        from models.user import User
        from models.job_model import Job
        print("Creating tables if they don't exist...")
        db.create_all()
        print("Migration complete. Jobs table verified.")

if __name__ == '__main__':
    migrate()
