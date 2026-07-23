import time
import logging
import os
from datetime import datetime
from extensions import db
from models.job_model import Job
from services.job_parser_service import JobParserService

# Setup Logger
logger = logging.getLogger('JobParserAgent')
logger.setLevel(logging.INFO)
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

fh = logging.FileHandler(os.path.join(log_dir, 'job_parser_agent.log'))
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(fh)

class JobParserAgent:
    def __init__(self, app):
        self.app = app
        self.service = JobParserService()
        
    def process(self):
        start_time = time.time()
        logger.info("Parsing started.")
        
        with self.app.app_context():
            # Find unprocessed jobs
            unprocessed_jobs = Job.query.filter(
                (Job.processed == False) | (Job.processed == None)
            ).all()
            
            processed_count = 0
            error_count = 0
            
            for job in unprocessed_jobs:
                try:
                    result = self.service.process_job(job.job_description, job.job_title)
                    
                    # Update job record
                    job.parsed_description = result['parsed_description']
                    job.technologies = result['technologies']
                    job.minimum_experience = result['minimum_experience']
                    job.maximum_experience = result['maximum_experience']
                    job.ai_domain = result['ai_domain']
                    job.classification_confidence = result['classification_confidence']
                    job.ai_summary = result['ai_summary']
                    
                    job.processed = True
                    job.processed_at = datetime.utcnow()
                    
                    db.session.add(job)
                    processed_count += 1
                    
                    logger.info(f"Job processed: {job.job_id} | Domain: {job.ai_domain} | Skills: {job.technologies}")
                    
                except Exception as e:
                    error_count += 1
                    logger.error(f"Error parsing job {job.job_id}: {str(e)}")
            
            try:
                db.session.commit()
                logger.info("Database updates saved.")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Database save error during parsing: {str(e)}")
                
        execution_time = round(time.time() - start_time, 2)
        logger.info(f"Parsing completed in {execution_time}s. Processed: {processed_count}, Errors: {error_count}")
