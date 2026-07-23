import unittest
import time
from app import create_app
from extensions import db
from models.user import User
from models.job_model import Job
from models.resume_model import ResumeAnalysis, StudentProfile
from models.recommendation_model import JobRecommendation
from models.orchestrator_model import SystemHealth, AgentExecutionLog, PipelineHistory, WorkflowStatus, AgentMetric
from services.monitoring_service import MonitoringService
from services.health_service import HealthService
from services.pipeline_service import PipelineService
from services.workflow_service import WorkflowService
from services.orchestration_service import OrchestrationService
from agents.master_orchestrator import MasterOrchestrator

class Phase7Tests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create test users
            admin = User(full_name='Admin', email='admin@test.com', role='admin')
            admin.set_password('admin123')
            
            student = User(full_name='Student', email='student@test.com', role='student')
            student.set_password('student123')
            
            db.session.add_all([admin, student])
            db.session.commit()
            self.student_id = student.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_service(self):
        with self.app.app_context():
            HealthService.log_health()
            health = HealthService.get_latest_health()
            self.assertIsNotNone(health)
            self.assertEqual(health.db_status, 'healthy')
            self.assertGreaterEqual(health.overall_health_score, 0)
            self.assertLessEqual(health.overall_health_score, 100)

    def test_monitoring_service(self):
        with self.app.app_context():
            exec_id = MonitoringService.start_agent_execution("TestAgent")
            log = AgentExecutionLog.query.filter_by(execution_id=exec_id).first()
            self.assertEqual(log.status, 'running')
            
            time.sleep(0.1) # force execution time > 0
            MonitoringService.complete_agent_execution(exec_id, records_processed=5)
            log = AgentExecutionLog.query.filter_by(execution_id=exec_id).first()
            self.assertEqual(log.status, 'completed')
            self.assertGreater(log.execution_time_ms, 0)
            self.assertEqual(log.records_processed, 5)
            
            metric = AgentMetric.query.filter_by(agent_name="TestAgent").first()
            self.assertIsNotNone(metric)
            self.assertEqual(metric.total_runs, 1)
            self.assertEqual(metric.successful_runs, 1)

    def test_pipeline_service(self):
        with self.app.app_context():
            pipeline_id = PipelineService.create_pipeline('test_pipeline', user_id=self.student_id)
            PipelineService.update_workflow_status('student', self.student_id, 'resume_intelligence', 'running')
            
            status = PipelineService.get_student_workflow_status(self.student_id)
            self.assertEqual(status.current_stage, 'resume_intelligence')
            self.assertEqual(status.status, 'running')
            
            PipelineService.complete_pipeline(pipeline_id, details={"test": "ok"})
            pipeline = PipelineHistory.query.filter_by(pipeline_id=pipeline_id).first()
            self.assertEqual(pipeline.status, 'completed')
            self.assertEqual(pipeline.details["test"], "ok")

    def test_master_orchestrator(self):
        with self.app.app_context():
            # Setup mock data so that agents don't crash
            # E.g. Job Parser expects Jobs to exist, Resume Agent expects analyses
            job = Job(job_id='t001', company_name='Test', job_title='Test', job_description='Test', 
                     source='Mock', ai_domain='Python', status='active')
            db.session.add(job)
            db.session.commit()
            
            # The workflow might try to hit the DB. We'll run the full pipeline.
            orchestrator = MasterOrchestrator(self.app)
            # This should log health, run all 4 agents safely, and log health again
            orchestrator.process()
            
            # Assert pipelines created
            history = PipelineHistory.query.filter_by(pipeline_type='master_orchestrator').first()
            self.assertIsNotNone(history)
            self.assertEqual(history.status, 'completed')

    def test_admin_control_center_route(self):
        self.client.post('/auth/login', data={'email': 'admin@test.com', 'password': 'admin123'})
        res = self.client.get('/admin/ai_control_center')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'AI Control Center', res.data)
        
    def test_student_dashboard_pipeline_status(self):
        self.client.post('/auth/login', data={'email': 'student@test.com', 'password': 'student123'})
        with self.app.app_context():
            PipelineService.update_workflow_status('student', self.student_id, 'recommendation', 'completed')
        res = self.client.get('/student/dashboard')
        self.assertEqual(res.status_code, 200)
        # Check if the titlecased status appears
        self.assertIn(b'Recommendation', res.data)

if __name__ == '__main__':
    unittest.main()
