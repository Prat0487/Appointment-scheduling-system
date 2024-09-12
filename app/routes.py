from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Appointment, User
from app import db
from datetime import datetime
import os

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/home')
def home():
    return render_template('home.html', user=current_user)

@routes.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(routes.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@routes.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('appointments.html', appointments=appointments)

@routes.route('/create_appointment', methods=['GET', 'POST'])
@login_required
def create_appointment():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']
    
        appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    
        new_appointment = Appointment(
            date=appointment_datetime,
            description=description,
            user_id=current_user.id
        )
    
        db.session.add(new_appointment)
        db.session.commit()
    
        flash('Appointment created successfully!', 'success')
        return redirect(url_for('routes.appointments'))

    return render_template('create_appointment.html')

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.home'))
        flash('Invalid username or password')
    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@routes.route('/edit_appointment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)

    if appointment.user_id != current_user.id:
        flash('You are not authorized to edit this appointment.', 'danger')
        return redirect(url_for('routes.appointments'))

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']
    
        appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    
        appointment.date = appointment_datetime
        appointment.description = description
    
        db.session.commit()
    
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('routes.appointments'))

    return render_template('edit_appointment.html', appointment=appointment)

@routes.route('/delete_appointment/<int:id>')
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)

    if appointment.user_id != current_user.id:
        flash('You are not authorized to delete this appointment.', 'danger')
        return redirect(url_for('routes.appointments'))

    db.session.delete(appointment)
    db.session.commit()

    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('routes.appointments'))
