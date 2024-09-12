from flask import Flask
from app.routes import routes
from app.models import db
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
app.register_blueprint(routes)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
