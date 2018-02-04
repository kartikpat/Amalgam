from flask import Flask

from config import app_config

from error-handlers import *

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .jobListing import jobListing as jobListing_blueprint
    app.register_blueprint(jobListing_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .assessment import assessment as assessment_blueprint
    app.register_blueprint(assessment_blueprint)

    return app

#app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = 'project/assessment/uploadedCSV/'
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# from users.views import users
# from jobListing.views import listingJob
# from assessment.views import listingQues

# app.register_blueprint(users)
# app.register_blueprint(listingJob)
# app.register_blueprint(listingQues)



# export FLASK_CONFIG=development
# $ export FLASK_APP=run.py
# $ flask run
