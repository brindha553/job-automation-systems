import time
import logging
import os
from extensions import db
from models.user import User
from models.resume_model import ResumeAnalysis
from services.recommendation_service import RecommendationService

# Logger setup
logger = logging.getLogger('RecommendationAgent')
logger.setLevel(logging.INFO)
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
fh = logging.FileHandler(os.path.join(log_dir, 'recommendation_agent.log'))
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
if not logger.handlers:
    logger.addHandler(fh)


class RecommendationAgent:
    """Agent 4 – matches student resume profiles against the parsed job pool."""

    def __init__(self, app):
        self.app = app

    def process(self):
        start = time.time()
        logger.info("Recommendation matching started.")

        with self.app.app_context():
            service = RecommendationService()

            # Find all students who have a processed resume
            student_ids = db.session.query(ResumeAnalysis.user_id).filter_by(
                processed=True
            ).distinct().all()
            student_ids = [row[0] for row in student_ids]

            total_recommendations = 0
            for uid in student_ids:
                try:
                    count = service.run_for_user(uid)
                    total_recommendations += count
                    logger.info(f"Student {uid}: {count} recommendations generated/updated.")
                except Exception as e:
                    logger.error(f"Error processing student {uid}: {e}")

            try:
                db.session.commit()
                logger.info("All recommendations committed to database.")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Commit error: {e}")

        elapsed = round(time.time() - start, 2)
        logger.info(
            f"Recommendation matching completed in {elapsed}s. "
            f"Students processed: {len(student_ids)}, Total recs: {total_recommendations}."
        )
