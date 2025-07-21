from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import University, Department, Student, Event, Ticket

class EventRegistrationTestCase(TestCase):
    def setUp(self):
        # Create a university, department, and student
        self.user = User.objects.create_user(username='student1', password='testpass')
        self.university = University.objects.create(
            name='Test Uni', user=User.objects.create_user('uni', 'uni@test.com', 'pass'),
            uni_id=1234567890123, address='Test Address', contact_email='uni@test.com', contact_phone='1234567890'
        )
        self.department = Department.objects.create(
            name='CS', university=self.university, user=User.objects.create_user('dept', 'dept@test.com', 'pass'),
            department_id=1234567890
        )
        self.student = Student.objects.create(
            user=self.user, university=self.university, full_name='Student One', phone='1234567890', is_approved=True
        )
        self.event = Event.objects.create(
            university=self.university, name='Test Event', start_date='2025-01-01', end_date='2025-01-02',
            start_time='10:00', end_time='12:00', fee=0, tickets=2, is_approved=True
        )
        self.client = Client()
        self.client.login(username='student1', password='testpass')

    def test_student_can_register_for_event(self):
        response = self.client.get(reverse('register', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after registration
        self.assertTrue(Ticket.objects.filter(user=self.user, event=self.event, payment_status='completed').exists())
        event = Event.objects.get(id=self.event.id)
        self.assertEqual(event.tickets, 1)  # Tickets should decrement

    def test_no_double_registration(self):
        # Register once
        self.client.get(reverse('register', args=[self.event.id]))
        # Try to register again
        response = self.client.get(reverse('register', args=[self.event.id]))
        self.assertContains(response, 'already registered', status_code=302)  # Should redirect with warning

    def test_no_registration_when_tickets_zero(self):
        self.event.tickets = 0
        self.event.save()
        response = self.client.get(reverse('register', args=[self.event.id]))
        self.assertContains(response, 'No tickets available', status_code=302)
        self.assertFalse(Ticket.objects.filter(user=self.user, event=self.event).exists())

    def test_pending_tickets_deleted_on_view(self):
        # Create a pending ticket
        Ticket.objects.create(event=self.event, user=self.user, payment_status='pending')
        self.client.get(reverse('student_tickets'))
        self.assertFalse(Ticket.objects.filter(user=self.user, payment_status='pending').exists())

# You can add more tests for paid events, department assignment, etc.

# Create your tests here.
