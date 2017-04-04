from flask import Flask

app = Flask(__name__)
app.secret_key ='sdlkfdklsjfljsd'

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

from users.views import users
from jobListing.views import listingJob



app.register_blueprint(users)
app.register_blueprint(listingJob)
