import os
from flask import Flask



from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta

app = Flask(__name__)





app.config["SECRET_KEY"] = '123456789'
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5000
app.config['DEBUG']= True


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
