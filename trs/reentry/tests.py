# from django.test import TestCase
# from django.contrib.auth.models import User, Group
# from .models import CareTeam, ParoleOfficer, Mentor, Need, Goal, Address, ReturningCitizen

# class ModelTestCase(TestCase):
#     def setUp(self):
#         # Create a user for testing
#         self.user = User.objects.create(username='testuser')

#         # Create a CareTeam
#         self.care_team = CareTeam.objects.create(name='Test Care Team', organization='Test Organization')

#         # Create Needs and Goals
#         self.need = Need.objects.create(need='Test Need', description='Test Description')
#         self.goal = Goal.objects.create(goal='Test Goal', description='Test Description')

#         # Create an Address
#         self.address = Address.objects.create(
#             address_1='123 Main St',
#             city='Test City',
#             state='CA',
#             zip_code='12345'
#         )

#     def test_care_team_model(self):
#         care_team = CareTeam.objects.get(name='Test Care Team')
#         self.assertEqual(care_team.organization, 'Test Organization')

#     def test_parole_officer_model(self):
#         parole_officer = ParoleOfficer.objects.create(user=self.user, organization='Test Organization')
#         parole_officer.care_teams.add(self.care_team)

#         self.assertIn(self.care_team, parole_officer.care_teams.all())

#         # Check if the Parole Officer Role group is created
#         self.assertTrue(parole_officer.user.groups.filter(name='Parole Officer Role').exists())

#     def test_mentor_model(self):
#         mentor = Mentor.objects.create(user=self.user, organization='Test Organization')
#         mentor.care_teams.add(self.care_team)

#         self.assertIn(self.care_team, mentor.care_teams.all())

#         # Check if the Mentor Role group is created
#         self.assertTrue(mentor.user.groups.filter(name='Mentor Role').exists())

#     def test_need_model(self):
#         need = Need.objects.get(need='Test Need')
#         self.assertEqual(need.description, 'Test Description')

#     def test_goal_model(self):
#         goal = Goal.objects.get(goal='Test Goal')
#         self.assertEqual(goal.description, 'Test Description')

#     def test_address_model(self):
#         address = Address.objects.get(address_1='123 Main St')
#         self.assertEqual(address.city, 'Test City')

#     def test_returning_citizen_model(self):
#         returning_citizen = ReturningCitizen.objects.create(
#             user=self.user,
#             first_name='John',
#             last_name='Doe',
#             address=self.address
#         )

#         self.assertEqual(returning_citizen.care_team.name, 'Care Team for John Doe')
#         self.assertIn(returning_citizen.user.groups.first().name, 'Returning Citizen Role')

#         # Test adding needs and goals to ReturningCitizen
#         returning_citizen.needs.add(self.need)
#         returning_citizen.goals.add(self.goal)

#         self.assertIn(self.need, returning_citizen.needs.all())
#         self.assertIn(self.goal, returning_citizen.goals.all())

from django.test import TestCase
from django.contrib.auth.models import User, Group
from .models import CareTeam, ParoleOfficer, Mentor, Need, Goal, Address, ReturningCitizen, Approval

class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(username='testuser')

        # Create a CareTeam
        self.care_team = CareTeam.objects.create(name='Test Care Team', organization='Test Organization')

        # Create Needs and Goals
        self.need = Need.objects.create(need='Test Need', description='Test Description')
        self.goal = Goal.objects.create(goal='Test Goal', description='Test Description')

        # Create an Address
        self.address = Address.objects.create(
            address_1='123 Main St',
            city='Test City',
            state='CA',
            zip_code='12345'
        )

    def test_care_team_model(self):
        care_team = CareTeam.objects.get(name='Test Care Team')
        self.assertEqual(care_team.organization, 'Test Organization')

    def test_parole_officer_model(self):
        parole_officer = ParoleOfficer.objects.create(user=self.user, organization='Test Organization')
        parole_officer.care_teams.add(self.care_team)

        self.assertIn(self.care_team, parole_officer.care_teams.all())

        # Check if the Parole Officer Role group is created
        self.assertTrue(parole_officer.user.groups.filter(name='Parole Officer Role').exists())

    def test_mentor_model(self):
        mentor = Mentor.objects.create(user=self.user, organization='Test Organization')
        mentor.care_teams.add(self.care_team)

        self.assertIn(self.care_team, mentor.care_teams.all())

        # Check if the Mentor Role group is created
        self.assertTrue(mentor.user.groups.filter(name='Mentor Role').exists())

    def test_need_model(self):
        need = Need.objects.get(need='Test Need')
        self.assertEqual(need.description, 'Test Description')

    def test_goal_model(self):
        goal = Goal.objects.get(goal='Test Goal')
        self.assertEqual(goal.description, 'Test Description')

    def test_address_model(self):
        address = Address.objects.get(address_1='123 Main St')
        self.assertEqual(address.city, 'Test City')

    def test_returning_citizen_model(self):
        returning_citizen = ReturningCitizen.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            address=self.address
        )

        self.assertEqual(returning_citizen.care_team.name, 'Care Team for John Doe')
        self.assertIn(returning_citizen.user.groups.first().name, 'Returning Citizen Role')

        # Test adding needs and goals to ReturningCitizen
        returning_citizen.needs.add(self.need)
        returning_citizen.goals.add(self.goal)

        self.assertIn(self.need, returning_citizen.needs.all())
        self.assertIn(self.goal, returning_citizen.goals.all())

    def test_approval_model(self):
        approval = Approval.objects.create(
            returning_citizen=ReturningCitizen.objects.create(user=self.user),
            parole_officer=ParoleOfficer.objects.create(user=User.objects.create(username='parole_officer_user')),
            approved=True
        )

        self.assertTrue(approval.returning_citizen.care_team.parole_officers.filter(user=approval.parole_officer.user).exists())
