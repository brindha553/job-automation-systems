import time
import logging
import os
from datetime import datetime
from extensions import db
from models.resume_model import ResumeAnalysis, ResumeSkill, ResumeProject, ResumeCertification, ResumeLanguage, StudentProfile
from services.resume_parser_service import ResumeParserService

logger = logging.getLogger('ResumeAgent')
logger.setLevel(logging.INFO)
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
fh = logging.FileHandler(os.path.join(log_dir, 'resume_agent.log'))
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
if not logger.handlers:
    logger.addHandler(fh)

class ResumeIntelligenceAgent:
    def __init__(self, app):
        self.app = app

    def process(self):
        start_time = time.time()
        logger.info("Resume parsing started.")
        
        with self.app.app_context():
            unprocessed = ResumeAnalysis.query.filter_by(processed=False).all()
            
            processed_count = 0
            
            for resume in unprocessed:
                try:
                    res = ResumeParserService.process(resume.file_path)
                    
                    resume.raw_text = res['raw_text']
                    resume.primary_domain = res['domain']
                    resume.domain_confidence = res['domain_confidence']
                    resume.domain_reason = res['domain_reason']
                    
                    profile = res['profile']
                    resume.professional_summary = profile['summary']
                    resume.career_objective = profile['objective']
                    resume.strengths = profile['strengths']
                    resume.weaknesses = profile['weaknesses']
                    resume.suggested_career_path = profile['career_path']
                    resume.learning_recommendations = profile['learning']
                    
                    resume.processed = True
                    resume.processed_at = datetime.utcnow()
                    
                    # Add Skills
                    for sk in res['skills']:
                        db.session.add(ResumeSkill(analysis_id=resume.id, skill_name=sk['name'], proficiency_score=sk['score']))
                        
                    # Add Projects
                    for p in res['projects']:
                        db.session.add(ResumeProject(analysis_id=resume.id, project_name=p['name'], description=p['desc']))
                        
                    # Add Certs
                    for c in res['certifications']:
                        db.session.add(ResumeCertification(analysis_id=resume.id, name=c))
                        
                    # Add Langs
                    for l in res['languages']:
                        db.session.add(ResumeLanguage(analysis_id=resume.id, language_name=l['name']))
                        
                    # Update Student Profile
                    student_prof = StudentProfile.query.filter_by(user_id=resume.user_id).first()
                    if not student_prof:
                        student_prof = StudentProfile(user_id=resume.user_id)
                        db.session.add(student_prof)
                        
                    top_skills = [sk['name'] for sk in sorted(res['skills'], key=lambda x: x['score'], reverse=True)[:5]]
                    student_prof.top_skills = ", ".join(top_skills)
                    student_prof.missing_skills = profile['learning']
                    
                    processed_count += 1
                    logger.info(f"Successfully processed resume for user {resume.user_id}. Domain: {res['domain']}")
                    
                except Exception as e:
                    logger.error(f"Error processing resume {resume.id}: {str(e)}")
                    
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logger.error(f"DB Error: {str(e)}")
                
        execution_time = round(time.time() - start_time, 2)
        logger.info(f"Resume parsing completed in {execution_time}s. Processed: {processed_count}")
