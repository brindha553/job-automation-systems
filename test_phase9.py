import unittest


from app import create_app
from extensions import db
from models.user import User
from models.job_model import Job
from models.placement_model import (Application, ApplicationHistory, Interview,
                                    Offer, Placement, PlacementAnalytics, PlacementNotification)
from services.application_service import ApplicationService
from services.interview_tracker_service import InterviewTrackerService
from services.offer_service import OfferService
from services.placement_service import PlacementService
from services.notification_service import NotificationService
from utils.placement_utils import calculate_placement_readiness, generate_ai_suggestions
from datetime import datetime, timedelta


class Phase9Tests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Create users
            admin = User(full_name='Admin', email='admin9@test.com', role='admin')
            admin.set_password('admin123')
            student = User(full_name='Student One', email='student9@test.com', role='student')
            student.set_password('student123')
            db.session.add_all([admin, student])
            db.session.flush()

            # Create job
            job = Job(job_id='j9001', company_name='TechCorp', job_title='Software Engineer',
                      job_description='Python Django', source='Test', ai_domain='Python', status='active')
            db.session.add(job)
            db.session.commit()
            self.student_id = student.id
            self.job_id = job.job_id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ========== Utility Tests ==========
    def test_readiness_calculation(self):
        score = calculate_placement_readiness({
            'application_success_rate': 80,
            'interview_success_rate': 70,
            'offer_conversion_rate': 100
        })
        self.assertGreater(score, 50)
        self.assertLessEqual(score, 100)

    def test_ai_suggestion_no_apps(self):
        suggestions = generate_ai_suggestions({'total_applications': 0})
        self.assertTrue(len(suggestions) > 0)
        self.assertIn("Start applying", suggestions[0])

    # ========== Application Tests ==========
    def test_apply_to_job(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            self.assertIsNotNone(app)
            self.assertEqual(app.status, 'Applied')

    def test_apply_duplicate_returns_existing(self):
        with self.app.app_context():
            app1 = ApplicationService.apply(self.student_id, self.job_id)
            app2 = ApplicationService.apply(self.student_id, self.job_id)
            self.assertEqual(app1.id, app2.id)

    def test_update_application_status(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            updated = ApplicationService.update_status(app.id, 'Shortlisted', 'Selected for interview')
            self.assertEqual(updated.status, 'Shortlisted')
            history = ApplicationHistory.query.filter_by(application_id=app.id, status='Shortlisted').first()
            self.assertIsNotNone(history)

    def test_application_stats(self):
        with self.app.app_context():
            ApplicationService.apply(self.student_id, self.job_id)
            stats = ApplicationService.get_application_stats(self.student_id)
            self.assertEqual(stats['total_applications'], 1)
            self.assertIn('application_success_rate', stats)

    # ========== Interview Tests ==========
    def test_schedule_interview(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            future = datetime.utcnow() + timedelta(days=2)
            interview = InterviewTrackerService.schedule_interview(app.id, 'Technical', future)
            self.assertEqual(interview.status, 'Scheduled')
            self.assertEqual(interview.interview_type, 'Technical')

    def test_update_interview(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            future = datetime.utcnow() + timedelta(days=2)
            interview = InterviewTrackerService.schedule_interview(app.id, 'HR', future)
            updated = InterviewTrackerService.update_interview(interview.id, status='Completed', score=80.0)
            self.assertEqual(updated.status, 'Completed')
            self.assertEqual(updated.score, 80.0)

    def test_interview_stats(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            future = datetime.utcnow() + timedelta(days=2)
            iv = InterviewTrackerService.schedule_interview(app.id, 'Technical', future)
            InterviewTrackerService.update_interview(iv.id, status='Completed', score=75.0)
            stats = InterviewTrackerService.get_interview_stats(self.student_id)
            self.assertEqual(stats['total_interviews'], 1)
            self.assertEqual(stats['cleared'], 1)

    # ========== Offer Tests ==========
    def test_create_offer(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            offer = OfferService.create_offer(app.id, 'TechCorp', 'Engineer', 12.5, 'Bangalore')
            self.assertIsNotNone(offer)
            self.assertEqual(offer.status, 'Pending')
            self.assertEqual(offer.package, 12.5)

    def test_accept_offer_creates_placement(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            offer = OfferService.create_offer(app.id, 'TechCorp', 'Engineer', 15.0)
            OfferService.respond_to_offer(offer.id, 'accept')
            placement = Placement.query.filter_by(student_id=self.student_id).first()
            self.assertIsNotNone(placement)
            updated_app = Application.query.get(app.id)
            self.assertEqual(updated_app.status, 'Placed')

    def test_reject_offer(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            offer = OfferService.create_offer(app.id, 'TechCorp', 'Engineer', 10.0)
            OfferService.respond_to_offer(offer.id, 'reject')
            updated = Offer.query.get(offer.id)
            self.assertEqual(updated.status, 'Rejected')

    def test_offer_stats(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            OfferService.create_offer(app.id, 'TechCorp', 'Engineer', 12.0)
            stats = OfferService.get_offer_stats(self.student_id)
            self.assertEqual(stats['total_offers'], 1)

    # ========== Placement Analytics Tests ==========
    def test_compute_analytics(self):
        with self.app.app_context():
            ApplicationService.apply(self.student_id, self.job_id)
            analytics = PlacementService.compute_analytics(self.student_id)
            self.assertIsNotNone(analytics)
            self.assertGreaterEqual(analytics.readiness_score, 0)
            self.assertIsNotNone(analytics.ai_suggestions)

    def test_admin_stats(self):
        with self.app.app_context():
            stats = PlacementService.get_admin_stats()
            self.assertIn('total_applications', stats)
            self.assertIn('placement_percentage', stats)

    # ========== Notification Tests ==========
    def test_notification_send_and_fetch(self):
        with self.app.app_context():
            NotificationService.send(self.student_id, 'Test Title', 'Test message', 'Info')
            notifs = NotificationService.get_unread(self.student_id)
            self.assertEqual(len(notifs), 1)
            self.assertEqual(notifs[0].title, 'Test Title')

    def test_notification_mark_read(self):
        with self.app.app_context():
            NotificationService.send(self.student_id, 'Test', 'Msg', 'Info')
            NotificationService.mark_all_read(self.student_id)
            notifs = NotificationService.get_unread(self.student_id)
            self.assertEqual(len(notifs), 0)

    # ========== Route Tests ==========
    def test_student_placement_center_route(self):
        self.client.post('/auth/login', data={'email': 'student9@test.com', 'password': 'student123'})
        res = self.client.get('/student/placement-center')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Placement Center', res.data)

    def test_admin_placement_intelligence_route(self):
        self.client.post('/auth/login', data={'email': 'admin9@test.com', 'password': 'admin123'})
        res = self.client.get('/admin/placement-intelligence')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Placement Intelligence', res.data)

    def test_apply_route(self):
        self.client.post('/auth/login', data={'email': 'student9@test.com', 'password': 'student123'})
        res = self.client.post(f'/student/apply/j9001', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        with self.app.app_context():
            app = Application.query.filter_by(student_id=self.student_id).first()
            self.assertIsNotNone(app)

    def test_admin_update_status_route(self):
        with self.app.app_context():
            app = ApplicationService.apply(self.student_id, self.job_id)
            app_id = app.id
        self.client.post('/auth/login', data={'email': 'admin9@test.com', 'password': 'admin123'})
        res = self.client.post(f'/admin/application/{app_id}/status',
                               data={'status': 'Shortlisted', 'notes': 'Selected'},
                               follow_redirects=True)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
