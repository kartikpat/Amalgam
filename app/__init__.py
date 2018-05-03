# third-party imports
from flask import Flask,make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)  
    
    print("Running in " + config_name + " mode!")  

    migrate = Migrate(app, db)

    from assessment.model import Employee
    from assessment.model import Department
    from assessment.model import Role

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .jobListing import jobListing as jobListing_blueprint
    app.register_blueprint(jobListing_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .assessment import assessment as assessment_blueprint
    app.register_blueprint(assessment_blueprint)

    @app.errorhandler(404)
    def not_found(error):
        message = error.description['message']
        if(message == ''): 
            message = 'missing parameters'

        return make_response(jsonify({
        'error': message,
        'status': error.description['status']
        }), 404) 

    @app.errorhandler(403)
    def forbidden(error):
        message = error.description['message']
        if(message == ''): 
            message = 'missing parameters'

        return make_response(jsonify({
        'error': message,
        'status': error.description['status']
        }), 404)    
    
    return app

#app.config['UPLOAD_FOLDER'] = 'project/assessment/uploadedCSV/'
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
