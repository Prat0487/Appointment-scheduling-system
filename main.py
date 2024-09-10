# main.py

import sqlite3
from datetime import datetime, timedelta

# Database setup
def create_database():
    conn = sqlite3.connect('appointment_system.db')
    c = conn.cursor()
    
    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, user_type TEXT)''')
    
    # Create Services table
    c.execute('''CREATE TABLE IF NOT EXISTS services
                 (id INTEGER PRIMARY KEY, name TEXT, duration INTEGER, price REAL)''')
    
    # Create Appointments table
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY, user_id INTEGER, service_id INTEGER, 
                  start_time DATETIME, end_time DATETIME,
                  FOREIGN KEY (user_id) REFERENCES users(id),
                  FOREIGN KEY (service_id) REFERENCES services(id))''')
    
    conn.commit()
    conn.close()

# User class
class User:
    def __init__(self, name, email, user_type):
        self.name = name
        self.email = email
        self.user_type = user_type  # 'provider' or 'client'
    
    def save_to_db(self):
        conn = sqlite3.connect('appointment_system.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, user_type) VALUES (?, ?, ?)",
                  (self.name, self.email, self.user_type))
        conn.commit()
        conn.close()

# Service class
class Service:
    def __init__(self, name, duration, price):
        self.name = name
        self.duration = duration  # in minutes
        self.price = price
    
    def save_to_db(self):
        conn = sqlite3.connect('appointment_system.db')
        c = conn.cursor()
        c.execute("INSERT INTO services (name, duration, price) VALUES (?, ?, ?)",
                  (self.name, self.duration, self.price))
        conn.commit()
        conn.close()

# Appointment class
class Appointment:
    def __init__(self, user_id, service_id, start_time):
        self.user_id = user_id
        self.service_id = service_id
        self.start_time = start_time
        self.end_time = None  # Will be calculated based on service duration
    
    def calculate_end_time(self):
        conn = sqlite3.connect('appointment_system.db')
        c = conn.cursor()
        c.execute("SELECT duration FROM services WHERE id = ?", (self.service_id,))
        duration = c.fetchone()[0]
        conn.close()
        
        self.end_time = self.start_time + timedelta(minutes=duration)
    
    def save_to_db(self):
        self.calculate_end_time()
        conn = sqlite3.connect('appointment_system.db')
        c = conn.cursor()
        c.execute("""INSERT INTO appointments 
                     (user_id, service_id, start_time, end_time) 
                     VALUES (?, ?, ?, ?)""",
                  (self.user_id, self.service_id, 
                   self.start_time.isoformat(), self.end_time.isoformat()))
        conn.commit()
        conn.close()

# Calendar class to manage appointments
class Calendar:
    @staticmethod
    def get_available_slots(date, service_id):
        # This is a simplified version. You'll need to expand this to check
        # against existing appointments and provider availability.
        conn = sqlite3.connect('appointment_system.db')
        c = conn.cursor()
        c.execute("SELECT duration FROM services WHERE id = ?", (service_id,))
        duration = c.fetchone()[0]
        conn.close()

        # For this example, we'll assume 9 AM to 5 PM availability
        start_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=9)
        end_time = start_time + timedelta(hours=8)
        
        slots = []
        current_slot = start_time
        while current_slot + timedelta(minutes=duration) <= end_time:
            slots.append(current_slot)
            current_slot += timedelta(minutes=duration)
        
        return slots

# Main application logic
def main():
    create_database()
    
    # Example usage
    user = User("John Doe", "john@example.com", "client")
    user.save_to_db()
    
    service = Service("Haircut", 30, 25.00)
    service.save_to_db()
    
    # Get available slots for a specific date and service
    date = datetime.now().date()
    available_slots = Calendar.get_available_slots(date, 1)  # Assuming service_id is 1
    
    if available_slots:
        # Book the first available slot
        appointment = Appointment(1, 1, available_slots[0])  # Assuming user_id is 1
        appointment.save_to_db()
        print(f"Appointment booked for {appointment.start_time}")
    else:
        print("No available slots")

if __name__ == "__main__":
    main()
