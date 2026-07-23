from app import create_app
from extensions import db

def migrate():
    app = create_app()
    with app.app_context():
        from models.recommendation_model import JobRecommendation, RecommendationHistory, RecommendationFeedback
        print("Creating Phase 6 recommendation tables safely...")
        db.create_all()
        print("Phase 6 Migration complete.")

if __name__ == '__main__':
    migrate()
