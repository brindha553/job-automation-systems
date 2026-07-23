from app import create_app
from extensions import db
from models.placement_model import Application, ApplicationHistory, Interview, Offer, Placement, PlacementAnalytics, PlacementNotification

app = create_app()

with app.app_context():
    db.create_all()
    print("Phase 9 Placement Models Migrated Successfully!")
