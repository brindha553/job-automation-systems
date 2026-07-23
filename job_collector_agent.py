import os
import hashlib
import time
import logging
from extensions import db
from models.job_model import Job
from services.job_service import LinkedInMockProvider, NaukriMockProvider

# Setup Logger
logger = logging.getLogger('JobCollectorAgent')
logger.setLevel(logging.INFO)
# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

fh = logging.FileHandler(os.path.join(log_dir, 'job_agent.log'))
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(fh)

class JobCollectorAgent:
    def __init__(self, app):
        self.app = app
        self.providers = [
            LinkedInMockProvider(),
            NaukriMockProvider()
        ]
        
    def generate_hash(self, company, title, location):
        unique_string = f"{company}_{title}_{location}".lower().strip()
        return hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

    def classify_domain(self, title, description, skills):
        text = f"{title} {description} {skills}".lower()
        
        domains = {
            'Full Stack': ['full stack', 'mern', 'mean', 'react and node'],
            'Frontend': ['frontend', 'front end', 'react', 'vue', 'angular', 'ui/ux'],
            'Backend': ['backend', 'back end', 'node', 'django', 'spring boot', 'flask'],
            'Machine Learning': ['machine learning', 'ml', 'pytorch', 'tensorflow'],
            'Artificial Intelligence': ['artificial intelligence', 'ai', 'llm', 'genai'],
            'Data Science': ['data science', 'data scientist', 'pandas', 'numpy'],
            'DevOps': ['devops', 'ci/cd', 'kubernetes', 'docker', 'jenkins'],
            'Cloud': ['cloud', 'aws', 'azure', 'gcp'],
            'Cyber Security': ['cyber security', 'security', 'penetration', 'soc'],
            'Software Testing': ['testing', 'qa', 'quality assurance', 'selenium'],
            'Salesforce': ['salesforce', 'sfdc', 'apex'],
            'Mobile Development': ['mobile', 'ios', 'android', 'flutter', 'react native'],
            'UI/UX': ['ui/ux', 'user interface', 'figma', 'designer']
        }
        
        for domain, keywords in domains.items():
            if any(kw in text for kw in keywords):
                return domain
        return 'Other'

    def process(self):
        start_time = time.time()
        logger.info("Job Collection started.")
        
        with self.app.app_context():
            total_collected = 0
            total_duplicates = 0
            total_saved = 0
            
            for provider in self.providers:
                logger.info(f"Collecting from provider: {provider.provider_name}")
                try:
                    raw_jobs = provider.collect_jobs()
                    for raw in raw_jobs:
                        total_collected += 1
                        normalized = provider.normalize(raw)
                        
                        if not provider.validate(normalized):
                            logger.warning(f"Validation failed for job: {normalized.get('job_title')}")
                            continue
                            
                        # Duplicate Detection
                        job_hash = self.generate_hash(
                            normalized['company_name'],
                            normalized['job_title'],
                            normalized['location']
                        )
                        
                        existing = Job.query.filter_by(job_id=job_hash).first()
                        if existing:
                            total_duplicates += 1
                            continue
                            
                        # Domain Classification
                        domain = self.classify_domain(
                            normalized['job_title'], 
                            normalized['job_description'], 
                            normalized['skills_required']
                        )
                        
                        # Save
                        job = Job(
                            job_id=job_hash,
                            company_name=normalized['company_name'],
                            job_title=normalized['job_title'],
                            job_description=normalized['job_description'],
                            skills_required=normalized['skills_required'],
                            location=normalized['location'],
                            salary=normalized['salary'],
                            experience=normalized['experience'],
                            employment_type=normalized['employment_type'],
                            apply_url=normalized['apply_url'],
                            source=normalized['source'],
                            domain=domain
                        )
                        db.session.add(job)
                        total_saved += 1
                        
                except Exception as e:
                    logger.error(f"Error processing provider {provider.provider_name}: {str(e)}")
            
            try:
                db.session.commit()
                logger.info("Database save successful.")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Database save error: {str(e)}")
                
        execution_time = round(time.time() - start_time, 2)
        logger.info(f"Collection completed in {execution_time}s. Found: {total_collected}, Saved: {total_saved}, Duplicates: {total_duplicates}")
