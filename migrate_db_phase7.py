from app import create_app
from extensions import db
from models.orchestrator_model import AgentExecutionLog, PipelineHistory, WorkflowStatus, SystemHealth, AgentMetric

app = create_app()

with app.app_context():
    print("Creating Phase 7 Orchestrator tables...")
    db.create_all()
    print("Tables created successfully.")
