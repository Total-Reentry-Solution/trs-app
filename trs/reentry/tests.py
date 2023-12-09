from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import CareTeam, ParoleOfficer, Mentor, ReturningCitizen

class CareTeamModelTest(TestCase):
    def test_care_team_str(self):
        care_team = CareTeam.objects.create(name='Test Care Team', organization='Test Organization')
        self.assertEqual(str(care_team), 'Test Care Team')

class ParoleOfficerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.care_team = CareTeam.objects.create(name='Test Care Team')
        self.parole_officer = ParoleOfficer.objects.create(user=self.user, organization='Test Organization')

    def test_parole_officer_str(self):
        self.assertEqual(str(self.parole_officer.user), 'testuser')

    def test_parole_officer_groups(self):
        self.assertTrue(self.user.groups.filter(name='Parole Officer Role').exists())

class MentorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.care_team = CareTeam.objects.create(name='Test Care Team')
        self.mentor = Mentor.objects.create(user=self.user, organization='Test Organization')

    def test_mentor_str(self):
        self.assertEqual(str(self.mentor.user), 'testuser')

    def test_mentor_groups(self):
        self.assertTrue(self.user.groups.filter(name='Mentor Role').exists())

class ReturningCitizenModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.returning_citizen = ReturningCitizen.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe'
        )

    def test_returning_citizen_str(self):
        self.assertEqual(str(self.returning_citizen.user), 'testuser')

    def test_returning_citizen_groups(self):
        self.assertTrue(self.user.groups.filter(name='Returning Citizen Role').exists())

    def test_returning_citizen_care_team_created(self):
        self.assertIsNotNone(self.returning_citizen.care_team)
