import unittest
from app import create_app
from extensions import db
from models.user import User
from models.job_model import Job
from agents.job_parser_agent import JobParserAgent

class Phase4Tests(unittest.TestCase):
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
            
            # Create unparsed jobs
            job1 = Job(
                job_id="test1",
                company_name="Tech Corp",
                job_title="Full Stack Developer",
                job_description="<p>Looking for a developer with 2-4 years experience in Python, React, and Node.js.</p>",
                source="Mock"
            )
            job2 = Job(
                job_id="test2",
                company_name="Data Inc",
                job_title="Data Scientist",
                job_description="<p>Must know Machine Learning, Python, Pandas. 5+ years experience.</p>",
                source="Mock"
            )
            db.session.add_all([job1, job2])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_job_parser_execution(self):
        with self.app.app_context():
            agent = JobParserAgent(self.app)
            agent.process()
            
            # Verify parsed state
            parsed_job1 = Job.query.filter_by(job_id="test1").first()
            self.assertTrue(parsed_job1.processed)
            self.assertIsNotNone(parsed_job1.processed_at)
            
            # Verify text cleaning
            self.assertNotIn('<p>', parsed_job1.parsed_description)
            
            # Verify Experience Extraction
            self.assertEqual(parsed_job1.minimum_experience, 2)
            self.assertEqual(parsed_job1.maximum_experience, 4)
            
            # Verify Skill Extraction
            self.assertIn("Python", parsed_job1.technologies)
            self.assertIn("React", parsed_job1.technologies)
            
            # Verify Classification
            self.assertEqual(parsed_job1.ai_domain, "Full Stack")
            
            # Verify AI Summary
            self.assertIn("Full Stack Developer", parsed_job1.ai_summary)

    def test_parser_admin_route(self):
        self.client.post('/auth/login', data={'email': 'admin@example.com', 'password': 'admin123'})
        
        # Run agent
        with self.app.app_context():
            agent = JobParserAgent(self.app)
            agent.process()
            
        res = self.client.get('/admin/parser')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'AI Job Parser Dashboard', res.data)
        self.assertIn(b'Tech Corp', res.data)
        
    def test_parser_search(self):
        self.client.post('/auth/login', data={'email': 'admin@example.com', 'password': 'admin123'})
        with self.app.app_context():
            agent = JobParserAgent(self.app)
            agent.process()
            
        res = self.client.get('/admin/parser?search=Data Inc')
        self.assertIn(b'Data Inc', res.data)
        self.assertNotIn(b'Tech Corp', res.data)

if __name__ == '__main__':
    unittest.main()
