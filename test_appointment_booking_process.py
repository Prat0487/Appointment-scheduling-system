import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from appointment_booking_process import book_appointment, display_available_time_slots, fetch_available_slots, create_and_add_appointment, generate_appointment_id, view_and_manage_appointments, reschedule_appointment, cancel_appointment, check_appointment_conflict

class TestAppointmentBookingProcess(unittest.TestCase):

    def setUp(self):
        self.existing_appointments = [
            {"id": "1", "service": "Haircut", "date": "2023-05-01", "time": "10:00 AM"},
            {"id": "2", "service": "Manicure", "date": "2023-05-02", "time": "2:00 PM"},
        ]

    @patch('builtins.input', side_effect=['1', '2023-05-15', '10:00 AM'])
    @patch('appointment_booking_process.fetch_available_slots')
    @patch('appointment_booking_process.create_and_add_appointment')
    def test_book_appointment(self, mock_create_add, mock_fetch_slots, mock_input):
        mock_fetch_slots.return_value = [
            {"date": "2023-05-15", "time": "10:00 AM"},
            {"date": "2023-05-15", "time": "2:00 PM"},
        ]
        mock_create_add.return_value = True

        result = book_appointment(self.existing_appointments)

        self.assertEqual(result['service'], 'Haircut')
        self.assertEqual(result['date'], '2023-05-15')
        self.assertEqual(result['time'], '10:00 AM')
        self.assertTrue(mock_create_add.called)

    @patch('appointment_booking_process.fetch_available_slots')
    def test_display_available_time_slots(self, mock_fetch_slots):
        mock_fetch_slots.return_value = [
            {"date": "2023-05-15", "time": "10:00 AM"},
            {"date": "2023-05-15", "time": "2:00 PM"},
        ]

        with patch('builtins.print') as mock_print:
            display_available_time_slots("Haircut")
            mock_print.assert_any_call("Available time slots for Haircut:")
            mock_print.assert_any_call("- 2023-05-15 at 10:00 AM")
            mock_print.assert_any_call("- 2023-05-15 at 2:00 PM")

    def test_fetch_available_slots(self):
        slots = fetch_available_slots("Haircut")
        self.assertIsInstance(slots, list)
        self.assertTrue(all(isinstance(slot, dict) for slot in slots))
        self.assertTrue(all('date' in slot and 'time' in slot for slot in slots))

    @patch('appointment_booking_process.add_to_database')
    @patch('appointment_booking_process.add_to_calendar')
    def test_create_and_add_appointment(self, mock_add_calendar, mock_add_database):
        appointment = {
            "id": "test_id",
            "service": "Haircut",
            "date": "2023-05-15",
            "time": "10:00 AM"
        }
        result = create_and_add_appointment(appointment)
        self.assertTrue(result)
        mock_add_database.assert_called_once_with(appointment)
        mock_add_calendar.assert_called_once_with(appointment)

    def test_generate_appointment_id(self):
        id1 = generate_appointment_id()
        id2 = generate_appointment_id()
        self.assertNotEqual(id1, id2)
        self.assertIsInstance(id1, str)
        self.assertIsInstance(id2, str)

    @patch('builtins.input', side_effect=['1', '3'])
    @patch('appointment_booking_process.manage_appointment')
    def test_view_and_manage_appointments(self, mock_manage, mock_input):
        view_and_manage_appointments(self.existing_appointments)
        mock_manage.assert_called_once_with(self.existing_appointments[0], self.existing_appointments)

    @patch('builtins.input', side_effect=['2023-05-20', '11:00 AM'])
    def test_reschedule_appointment(self, mock_input):
        appointment = self.existing_appointments[0].copy()
        reschedule_appointment(appointment, self.existing_appointments)
        self.assertEqual(appointment['date'], '2023-05-20')
        self.assertEqual(appointment['time'], '11:00 AM')

    @patch('builtins.input', return_value='y')
    def test_cancel_appointment(self, mock_input):
        appointment = self.existing_appointments[0].copy()
        cancel_appointment(appointment, self.existing_appointments)
        self.assertNotIn(appointment, self.existing_appointments)

    def test_check_appointment_conflict(self):
        self.assertTrue(check_appointment_conflict('2023-05-01', '10:00 AM', self.existing_appointments))
        self.assertFalse(check_appointment_conflict('2023-05-01', '11:00 AM', self.existing_appointments))

if __name__ == '__main__':
    unittest.main()
