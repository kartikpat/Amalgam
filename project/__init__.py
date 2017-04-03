from flask import Flask

app = Flask(__name__)

app.secret_key ='sdlkfdklsjfljsd'

from users.views import users
from jobListing.views import listingJob


app.register_blueprint(users)
app.register_blueprint(listingJob)