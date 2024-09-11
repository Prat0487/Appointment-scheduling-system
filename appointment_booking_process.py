def book_appointment(existing_appointments):
    """Book a new appointment."""
    print("Booking a new appointment")
    service = input("Enter service: ")
    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM): ")

    if check_appointment_conflict(date, time, existing_appointments):
        print("Sorry, there's already an appointment at this time. Please choose another time.")
        return False

    new_appointment = create_and_add_appointment(service, date, time)
    existing_appointments.append(new_appointment)
    print(f"Appointment booked successfully. Appointment ID: {new_appointment['id']}")
    return True

def view_and_manage_appointments(existing_appointments):
    """View and manage existing appointments."""
    if not existing_appointments:
        print("No appointments found.")
        return
  
    print("Existing Appointments:")
    for idx, appointment in enumerate(existing_appointments, 1):
        print(f"{idx}. Service: {appointment['service']}, Date: {appointment['date']}, Time: {appointment['time']}")
  
    while True:
        choice = input("Enter the number of the appointment to manage (or 'q' to quit): ")
        if choice.lower() == 'q':
            break
      
        try:
            index = int(choice) - 1
            if 0 <= index < len(existing_appointments):
                manage_appointment(existing_appointments[index], existing_appointments)
            else:
                print("Invalid appointment number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

def manage_appointment(appointment, existing_appointments):
    """Manage a specific appointment."""
    print(f"\nManaging appointment: Service: {appointment['service']}, Date: {appointment['date']}, Time: {appointment['time']}")
  
    while True:
        print("\n1. Reschedule appointment")
        print("2. Cancel appointment")
        print("3. Back to appointment list")
      
        choice = input("Enter your choice (1-3): ")
      
        if choice == '1':
            reschedule_appointment(appointment, existing_appointments)
        elif choice == '2':
            cancel_appointment(appointment, existing_appointments)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def reschedule_appointment(appointment, existing_appointments):
    """Reschedule an existing appointment."""
    print(f"Rescheduling appointment: {appointment}")
    new_date = input("Enter new date (YYYY-MM-DD): ")
    new_time = input("Enter new time (HH:MM): ")
  
    if check_appointment_conflict(new_date, new_time, existing_appointments):
        print("Sorry, there's already an appointment at this time. Please choose another time.")
        return

    appointment['date'] = new_date
    appointment['time'] = new_time
    print(f"Appointment rescheduled to {new_date} at {new_time}")

def cancel_appointment(appointment, existing_appointments):
    """Cancel an existing appointment."""
    print(f"Cancelling appointment: {appointment}")
  
    confirm = input("Are you sure you want to cancel this appointment? (y/n): ")
    if confirm.lower() == 'y':
        existing_appointments.remove(appointment)
        print("Appointment cancelled successfully.")
    else:
        print("Cancellation aborted.")

def check_appointment_conflict(date, time, existing_appointments):
    """Check if there's a conflict with existing appointments."""
    for appointment in existing_appointments:
        if appointment['date'] == date and appointment['time'] == time:
            return True
    return False

def display_available_time_slots(available_slots):
    """Display available time slots."""
    print("Available Time Slots:")
    for slot in available_slots:
        print(f"Date: {slot['date']}, Time: {slot['time']}")

def fetch_available_slots():
    """Fetch available time slots."""
    # This is a placeholder function. In a real system, this would fetch data from a database or external service.
    return [
        {"date": "2023-05-01", "time": "09:00"},
        {"date": "2023-05-01", "time": "10:00"},
        {"date": "2023-05-01", "time": "11:00"},
        {"date": "2023-05-02", "time": "14:00"},
        {"date": "2023-05-02", "time": "15:00"},
        {"date": "2023-05-02", "time": "16:00"},
    ]

def create_and_add_appointment(service, date, time):
    """Create and add a new appointment."""
    appointment_id = generate_appointment_id()
    return {
        "id": appointment_id,
        "service": service,
        "date": date,
        "time": time
    }

def generate_appointment_id():
    """Generate a unique appointment ID."""
    # This is a simple implementation. In a real system, you might use a more sophisticated method.
    import random
    return f"APT-{random.randint(1000, 9999)}"

def add_to_calendar(appointment):
    """Add appointment to calendar."""
    # This is a placeholder function. In a real system, this would integrate with a calendar service.
    print(f"Adding appointment to calendar: {appointment}")
