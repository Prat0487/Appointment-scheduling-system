from flask import Flask
from app import app
from app import db
from app.models import User, Appointment

app = Flask(__name__)
@app.route('/test1')
def test():
    return "Test route working"


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Appointment': Appointment}

if __name__ == '__main__':
    app.run(debug=True)

app.run(debug=True)