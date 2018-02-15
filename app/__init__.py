from flask import Flask

from config import app_config

from errorHandlers import *
from flask import make_response,jsonify
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # print("Running in " + config_name + " mode!")
    # print(app_config[config_name]["FLASK_DEBUG"])
    # if() {
    #     app.debug = True
    # }

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .jobListing import jobListing as jobListing_blueprint
    app.register_blueprint(jobListing_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .assessment import assessment as assessment_blueprint
    app.register_blueprint(assessment_blueprint)

    return app

#app.config['UPLOAD_FOLDER'] = 'project/assessment/uploadedCSV/'
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
