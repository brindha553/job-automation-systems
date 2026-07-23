from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from agents.master_orchestrator import MasterOrchestrator

scheduler = BackgroundScheduler(daemon=True)
_app_ref = None

def run_master_orchestrator():
    if _app_ref:
        MasterOrchestrator(_app_ref).process()

def init_scheduler(app):
    global _app_ref
    _app_ref = app

    # Run full multi-agent pipeline every 15 minutes
    scheduler.add_job(func=run_master_orchestrator, trigger="interval", minutes=15)

    if not scheduler.running:
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
