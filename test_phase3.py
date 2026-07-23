import unittest
from app import create_app
from extensions import db
from models.user import User
from models.job_model import Job
from agents.job_collector_agent import JobCollectorAgent

class Phase3Tests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            
            # Create admin user
            admin = User(full_name='Admin', email='admin@example.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_job_collection_and_duplicate_detection(self):
        with self.app.app_context():
            agent = JobCollectorAgent(self.app)
            
            # First run: Should insert 3 jobs (2 from LinkedIn Mock, 1 from Naukri Mock)
            agent.process()
            job_count = Job.query.count()
            self.assertEqual(job_count, 3)
            
            # Second run: Should detect duplicates and insert 0 new jobs
            agent.process()
            job_count_after = Job.query.count()
            self.assertEqual(job_count_after, 3)

    def test_domain_classification(self):
        with self.app.app_context():
            agent = JobCollectorAgent(self.app)
            agent.process()
            
            # Tech Innovators should be Full Stack
            fs_job = Job.query.filter_by(company_name='Tech Innovators').first()
            self.assertIsNotNone(fs_job)
            # The description says "Python and React" and title is "Full Stack"
            # Our classifier assigns "Full Stack" based on "full stack" keyword
            self.assertEqual(fs_job.domain, 'Full Stack')
            
            # Data Solutions should be Data Science
            ds_job = Job.query.filter_by(company_name='Data Solutions').first()
            self.assertEqual(ds_job.domain, 'Machine Learning')

    def test_admin_jobs_route(self):
        # Login as admin
        self.client.post('/auth/login', data={'email': 'admin@example.com', 'password': 'admin123'})
        
        # Run collector to populate jobs
        with self.app.app_context():
            agent = JobCollectorAgent(self.app)
            agent.process()
            
        res = self.client.get('/admin/jobs')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Job Intelligence Center', res.data)
        self.assertIn(b'Tech Innovators', res.data)

    def test_admin_jobs_search(self):
        self.client.post('/auth/login', data={'email': 'admin@example.com', 'password': 'admin123'})
        with self.app.app_context():
            agent = JobCollectorAgent(self.app)
            agent.process()
            
        res = self.client.get('/admin/jobs?search=Data Solutions')
        self.assertIn(b'Data Solutions', res.data)
        self.assertNotIn(b'CloudTech', res.data)

if __name__ == '__main__':
    unittest.main()
