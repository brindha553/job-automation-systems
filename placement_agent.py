import time
from utils.placement_utils import setup_placement_logger

logger = setup_placement_logger()


class PlacementAgent:
    """
    Agent 6: Placement Intelligence Agent.
    Iterates all active students, computes placement analytics,
    and dispatches notifications for any critical status changes.
    """

    def __init__(self, app):
        self.app = app

    def process(self):
        start = time.time()
        logger.info("PlacementAgent started")
        try:
            with self.app.app_context():
                self._run()
        except Exception as e:
            logger.error(f"PlacementAgent failed: {e}", exc_info=True)
        elapsed = round(time.time() - start, 2)
        logger.info(f"PlacementAgent finished in {elapsed}s")

    def _run(self):
        from models.user import User
        from models.placement_model import Application
        from services.placement_service import PlacementService
        from services.notification_service import NotificationService

        students = User.query.filter_by(role='student').all()
        processed = 0
        for student in students:
            try:
                # Only process students who have at least one application
                app_count = Application.query.filter_by(student_id=student.id).count()
                if app_count == 0:
                    continue

                analytics = PlacementService.compute_analytics(student.id)

                # Notify student about readiness changes
                if analytics.readiness_score < 30:
                    NotificationService.send(
                        student_id=student.id,
                        title="Placement Readiness Alert",
                        message="Your placement readiness score is low. Follow AI suggestions to improve.",
                        type="Alert"
                    )
                elif analytics.readiness_score >= 80:
                    NotificationService.send(
                        student_id=student.id,
                        title="You're Highly Placement Ready!",
                        message=f"Your placement readiness is {analytics.readiness_score}%. Keep it up!",
                        type="Success"
                    )
                processed += 1
            except Exception as e:
                logger.error(f"Error processing student {student.id}: {e}")

        logger.info(f"PlacementAgent: processed {processed}/{len(students)} students")
