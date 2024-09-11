from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Appointment, User
from app import db
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', user=current_user)
    return render_template('home.html')

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
