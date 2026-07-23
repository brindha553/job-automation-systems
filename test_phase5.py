import unittest
import tempfile
import os
from app import create_app
from extensions import db
from models.user import User
from models.resume_model import ResumeAnalysis, ResumeSkill, StudentProfile
from agents.resume_intelligence_agent import ResumeIntelligenceAgent
from services.resume_skill_service import ResumeSkillService
from services.resume_classifier_service import ResumeClassifierService
from utils.resume_utils import ResumeUtils

class Phase5Tests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            admin = User(full_name='Admin', email='admin@test.com', role='admin')
            admin.set_password('admin123')
            student = User(full_name='Student One', email='student@test.com', role='student')
            student.set_password('student123')
            db.session.add_all([admin, student])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_txt_file_extraction(self):
        """TXT parsing via ResumeUtils"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as f:
            f.write("Experienced Python and React Developer. 2-4 years experience in full stack development.")
            tmp_path = f.name
        text = ResumeUtils.extract_text(tmp_path)
        os.unlink(tmp_path)
        self.assertIn("Python", text)
        self.assertIn("React", text)

    def test_skill_extraction(self):
        """Skill extraction from raw text"""
        text = "I have expertise in Python, React, Docker and AWS."
        skills = ResumeSkillService.extract_skills(text)
        self.assertIn('Python', skills)
        self.assertIn('React', skills)
        self.assertIn('Docker', skills)
        self.assertIn('AWS', skills)

    def test_domain_classification(self):
        """Domain classification from text + skills"""
        text = "Machine learning engineer with expertise in TensorFlow and Scikit-learn."
        skills = ['Python', 'TensorFlow', 'Scikit-learn']
        domain, confidence, reason = ResumeClassifierService.classify(text, skills)
        self.assertEqual(domain, 'Machine Learning')
        self.assertGreater(confidence, 0.0)

    def test_full_pipeline_with_txt_resume(self):
        """Full agent pipeline from file upload to DB storage"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as f:
            f.write("Full Stack Developer. Experienced in React, Node.js, Python. Projects: E-commerce site. Certifications: AWS Certified.")
            tmp_path = f.name

        with self.app.app_context():
            student = User.query.filter_by(email='student@test.com').first()
            analysis = ResumeAnalysis(user_id=student.id, file_path=tmp_path)
            db.session.add(analysis)
            db.session.commit()

            agent = ResumeIntelligenceAgent(self.app)
            agent.process()

            analysis = ResumeAnalysis.query.filter_by(user_id=student.id).first()
            self.assertTrue(analysis.processed)
            self.assertIsNotNone(analysis.processed_at)
            self.assertIsNotNone(analysis.primary_domain)
            self.assertIsNotNone(analysis.professional_summary)
            # Skills should be stored
            skills = ResumeSkill.query.filter_by(analysis_id=analysis.id).all()
            self.assertGreater(len(skills), 0)
            # Student profile should be updated
            profile = StudentProfile.query.filter_by(user_id=student.id).first()
            self.assertIsNotNone(profile)
            self.assertIsNotNone(profile.top_skills)

        os.unlink(tmp_path)

    def test_admin_resume_intelligence_route(self):
        """Admin route renders successfully"""
        self.client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'admin123'})
        res = self.client.get('/admin/resume_intelligence')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Resume Intelligence', res.data)

    def test_student_resume_intelligence_route(self):
        """Student resume_intelligence page renders correctly"""
        self.client.post('/auth/login', data={'email': 'student@test.com', 'password': 'student123'})
        res = self.client.get('/student/resume_intelligence')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'AI Resume Intelligence', res.data)

    def test_student_can_upload_resume(self):
        """Student can upload a TXT resume via the form"""
        self.client.post('/auth/login', data={'email': 'student@test.com', 'password': 'student123'})
        data = {
            'resume': (b'Python developer with 3 years experience in Machine Learning.', 'resume.txt')
        }
        # Use the correct format for file upload in Flask test client
        from io import BytesIO
        data = {'resume': (BytesIO(b'Python developer with 3 years experience in Machine Learning.'), 'resume.txt')}
        res = self.client.post('/student/resume_intelligence',
                               data=data,
                               content_type='multipart/form-data',
                               follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_corrupt_file_does_not_crash(self):
        """Corrupted file gracefully returns empty string"""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False, mode='wb') as f:
            f.write(b'this is not a real PDF file content')
            tmp_path = f.name
        text = ResumeUtils.extract_text(tmp_path)
        os.unlink(tmp_path)
        # Should return empty string, not raise exception
        self.assertIsInstance(text, str)

if __name__ == '__main__':
    unittest.main()
