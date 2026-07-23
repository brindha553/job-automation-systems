from services.orchestration_service import OrchestrationService
from services.health_service import HealthService
from utils.orchestration_utils import setup_orchestrator_logger
import time

logger = setup_orchestrator_logger()

class MasterOrchestrator:
    def __init__(self, app):
        self.app = app
        self.orchestration_service = OrchestrationService(app)
        
    def process(self):
        logger.info("Master Orchestrator Waking Up...")
        start_time = time.time()
        
        # 1. Log System Health Before Run
        with self.app.app_context():
            HealthService.log_health()
            
        # 2. Execute Full Multi-Agent Pipeline
        self.orchestration_service.execute_master_pipeline()
        
        # 3. Log System Health After Run
        with self.app.app_context():
            HealthService.log_health()
            
        duration = time.time() - start_time
        logger.info(f"Master Orchestrator Run Completed in {duration:.2f}s")

class WorkflowManager:
    # Optional wrapper for specific manual workflow triggers
    def __init__(self, app):
        self.app = app
        self.orchestration_service = OrchestrationService(app)
        
    def trigger_student_workflow(self, student_id):
        self.orchestration_service.execute_student_workflow(student_id)
