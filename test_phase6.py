import unittest
import tempfile
import os
from io import BytesIO
from app import create_app
from extensions import db
from models.user import User
from models.job_model import Job
from models.resume_model import ResumeAnalysis, ResumeSkill, ResumeProject, ResumeCertification
from models.recommendation_model import JobRecommendation, RecommendationHistory
from services.similarity_service import SimilarityService
from services.scoring_service import ScoringService
from services.recommendation_engine import RecommendationEngine
from services.recommendation_service import RecommendationService
from agents.recommendation_agent import RecommendationAgent
from utils.recommendation_utils import parse_skill_list, compute_overlap, priority_from_score


class Phase6Tests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Admin
            admin = User(full_name='Admin', email='admin@test.com', role='admin')
            admin.set_password('admin123')

            # Student
            student = User(full_name='Student One', email='student@test.com', role='student')
            student.set_password('student123')

            db.session.add_all([admin, student])
            db.session.commit()

            # Parsed job
            job = Job(
                job_id='j001',
                company_name='TechCorp',
                job_title='Full Stack Developer',
                job_description='React, Python, Docker required.',
                skills_required='Python, React, Docker',
                source='Mock',
                ai_domain='Full Stack',
                processed=True,
                status='active'
            )
            db.session.add(job)
            db.session.commit()

            # Resume analysis for student
            ra = ResumeAnalysis(
                user_id=student.id,
                file_path='/fake/resume.txt',
                primary_domain='Full Stack',
                domain_confidence=0.85,
                professional_summary='Full stack dev.',
                career_objective='Seeking Full Stack role.',
                strengths='Communication, Python, problem solving.',
                processed=True
            )
            db.session.add(ra)
            db.session.commit()

            db.session.add(ResumeSkill(analysis_id=ra.id, skill_name='Python',    proficiency_score=80))
            db.session.add(ResumeSkill(analysis_id=ra.id, skill_name='React',     proficiency_score=75))
            db.session.add(ResumeProject(analysis_id=ra.id, project_name='E-commerce', description='Used Python and React'))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # --- Unit tests -------------------------------------------------------

    def test_skill_overlap(self):
        matching, missing = compute_overlap(['python', 'react'], ['python', 'docker'])
        self.assertIn('python', matching)
        self.assertIn('docker', missing)
        self.assertNotIn('react', missing)

    def test_missing_skill_detection(self):
        student_skills = ['python', 'react']
        job_skills = ['python', 'docker', 'kubernetes']
        _, missing = compute_overlap(student_skills, job_skills)
        self.assertIn('docker', missing)
        self.assertIn('kubernetes', missing)

    def test_domain_score_match(self):
        score = SimilarityService.domain_score('Full Stack', 'Full Stack')
        self.assertEqual(score, 1.0)

    def test_domain_score_mismatch(self):
        score = SimilarityService.domain_score('Full Stack', 'Machine Learning')
        self.assertEqual(score, 0.0)

    def test_skill_score_partial(self):
        score = SimilarityService.skill_score('Python, React', 'Python, React, Docker')
        self.assertGreater(score, 0.5)
        self.assertLess(score, 1.0)

    def test_priority_levels(self):
        self.assertEqual(priority_from_score(80), 'high')
        self.assertEqual(priority_from_score(50), 'medium')
        self.assertEqual(priority_from_score(20), 'low')

    # --- Integration tests ------------------------------------------------

    def test_scoring_service(self):
        with self.app.app_context():
            job = Job.query.first()
            resume = ResumeAnalysis.query.first()
            skills = ResumeSkill.query.all()
            projects = ResumeProject.query.all()
            certs = ResumeCertification.query.all()

            result = ScoringService.compute(None, resume, skills, projects, certs, job)
            self.assertIn('overall_match_score', result)
            self.assertGreaterEqual(result['overall_match_score'], 0)
            self.assertLessEqual(result['overall_match_score'], 100)
            self.assertIn(result['priority_level'], ['high', 'medium', 'low'])

    def test_full_pipeline_and_db_storage(self):
        with self.app.app_context():
            agent = RecommendationAgent(self.app)
            agent.process()

            recs = JobRecommendation.query.all()
            self.assertGreater(len(recs), 0)

            rec = recs[0]
            self.assertIsNotNone(rec.overall_match_score)
            self.assertIsNotNone(rec.matching_skills)
            self.assertIsNotNone(rec.reasons_for_recommendation)

            history = RecommendationHistory.query.all()
            self.assertGreater(len(history), 0)

    def test_ranking_order(self):
        with self.app.app_context():
            # Add a second job with lower expected match
            job2 = Job(
                job_id='j002', company_name='DataCo', job_title='Data Scientist',
                job_description='Pandas, TensorFlow, R required.', skills_required='Pandas, TensorFlow, R',
                source='Mock', ai_domain='Machine Learning', processed=True, status='active'
            )
            db.session.add(job2)
            db.session.commit()

            agent = RecommendationAgent(self.app)
            agent.process()

            student = User.query.filter_by(email='student@test.com').first()
            recs = JobRecommendation.query.filter_by(
                user_id=student.id
            ).order_by(JobRecommendation.overall_match_score.desc()).all()
            self.assertGreaterEqual(len(recs), 2)
            # Scores should be descending
            for i in range(len(recs) - 1):
                self.assertGreaterEqual(recs[i].overall_match_score, recs[i+1].overall_match_score)

    # --- Route tests ------------------------------------------------------

    def test_student_recommendations_route(self):
        self.client.post('/auth/login', data={'email': 'student@test.com', 'password': 'student123'})
        with self.app.app_context():
            RecommendationAgent(self.app).process()
        res = self.client.get('/student/recommendations')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'AI Job Recommendations', res.data)

    def test_admin_analytics_route(self):
        self.client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'admin123'})
        with self.app.app_context():
            RecommendationAgent(self.app).process()
        res = self.client.get('/admin/recommendation_analytics')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Recommendation Analytics', res.data)


if __name__ == '__main__':
    unittest.main()
