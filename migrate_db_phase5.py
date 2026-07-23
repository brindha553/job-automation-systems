import sqlite3
import os
from app import create_app
from extensions import db

def migrate():
    app = create_app()
    with app.app_context():
        from models.resume_model import StudentProfile, ResumeAnalysis, ResumeSkill, ResumeProject, ResumeCertification, ResumeLanguage
        print("Creating Phase 5 tables safely...")
        db.create_all()
        print("Phase 5 Migration complete.")

if __name__ == '__main__':
    migrate()
