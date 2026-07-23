from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import config
import os

from extensions import db, bcrypt, login_manager, csrf, limiter, cache
from flask_talisman import Talisman
from flask import render_template


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    if app.config.get('TESTING'):
        app.config['WTF_CSRF_ENABLED'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    if not app.config.get('TESTING'):
        Talisman(app, content_security_policy=None)



    # Make sure upload folders exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resumes'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'jobs'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'database'), exist_ok=True)

    from controllers.main import main
    from controllers.auth import auth
    from controllers.student import student
    from controllers.admin import admin
    from controllers.placement import placement

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(student, url_prefix='/student')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(placement)


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        from models.user import User
        from models.job_model import Job
        from models.placement_model import (Application, ApplicationHistory,
            Interview, Offer, Placement, PlacementAnalytics, PlacementNotification)
        db.create_all()
    
    # Initialize background scheduler
    from agents.scheduler import init_scheduler
    init_scheduler(app)
    
    app.run(debug=True, use_reloader=False)
