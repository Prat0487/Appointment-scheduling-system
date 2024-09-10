import unittest
from datetime import datetime, timedelta
from main import User, Service, Appointment, Calendar, create_database

class TestAppointmentSystem(unittest.TestCase):
    def setUp(self):
        create_database()

    def test_user_creation(self):
        user = User("Test User", "test@example.com", "client")
        user.save_to_db()
        # Add assertion to check if user was saved correctly

    def test_service_creation(self):
        service = Service("Test Service", 60, 50.00)
        service.save_to_db()
        # Add assertion to check if service was saved correctly

    def test_appointment_creation(self):
        user = User("Test User", "test@example.com", "client")
        user.save_to_db()
        service = Service("Test Service", 60, 50.00)
        service.save_to_db()
        start_time = datetime.now() + timedelta(days=1)
        appointment = Appointment(1, 1, start_time)
        appointment.save_to_db()
        # Add assertion to check if appointment was saved correctly

    def test_calendar_available_slots(self):
        service = Service("Test Service", 60, 50.00)
        service.save_to_db()
        date = datetime.now().date() + timedelta(days=1)
        slots = Calendar.get_available_slots(date, 1)
        self.assertTrue(len(slots) > 0)

if __name__ == '__main__':
    unittest.main()
