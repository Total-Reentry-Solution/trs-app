from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import (
    CareTeam,
    ParoleOfficer,
    Mentor,
    Need,
    Goal,
    Address,
    ReturningCitizen,
    Approval,
    Questionnaire,
    Question,
    UserResponse,
)

from .forms import create_dynamic_questionnaire_form

from django.urls import reverse


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create(username="testuser")

        # Create a CareTeam
        self.care_team = CareTeam.objects.create(
            name="Test Care Team", organization="Test Organization"
        )

        # Create Needs and Goals
        self.need = Need.objects.create(
            need="Test Need", description="Test Description"
        )
        self.goal = Goal.objects.create(
            goal="Test Goal", description="Test Description"
        )

        # Create an Address
        self.address = Address.objects.create(
            address_1="123 Main St", city="Test City", state="CA", zip_code="12345"
        )
        self.questionnaire = Questionnaire.objects.create(
            title="Test Questionnaire", description="Description"
        )
        self.question = Question.objects.create(
            questionnaire=self.questionnaire, text="Test Question", order=1
        )
        self.user_response = UserResponse.objects.create(
            user=self.user,
            questionnaire=self.questionnaire,
            question=self.question,
            response="testuser's response to 'Test Question'",
        )

    def test_care_team_model(self):
        care_team = CareTeam.objects.get(name="Test Care Team")
        self.assertEqual(care_team.organization, "Test Organization")

    def test_parole_officer_model(self):
        parole_officer = ParoleOfficer.objects.create(
            user=self.user, organization="Test Organization"
        )
        parole_officer.care_teams.add(self.care_team)

        self.assertIn(self.care_team, parole_officer.care_teams.all())

        # Check if the Parole Officer Role group is created
        self.assertTrue(
            parole_officer.user.groups.filter(name="Parole Officer Role").exists()
        )

    def test_mentor_model(self):
        mentor = Mentor.objects.create(user=self.user, organization="Test Organization")
        mentor.care_teams.add(self.care_team)

        self.assertIn(self.care_team, mentor.care_teams.all())

        # Check if the Mentor Role group is created
        self.assertTrue(mentor.user.groups.filter(name="Mentor Role").exists())

    def test_need_model(self):
        need = Need.objects.get(need="Test Need")
        self.assertEqual(need.description, "Test Description")

    def test_goal_model(self):
        goal = Goal.objects.get(goal="Test Goal")
        self.assertEqual(goal.description, "Test Description")

    def test_address_model(self):
        address = Address.objects.get(address_1="123 Main St")
        self.assertEqual(address.city, "Test City")

    def test_returning_citizen_model(self):
        returning_citizen = ReturningCitizen.objects.create(
            user=self.user, first_name="John", last_name="Doe", address=self.address
        )

        self.assertEqual(returning_citizen.care_team.name, "Care Team for John Doe")
        self.assertIn(
            returning_citizen.user.groups.first().name, "Returning Citizen Role"
        )

        # Test adding needs and goals to ReturningCitizen
        returning_citizen.needs.add(self.need)
        returning_citizen.goals.add(self.goal)

        self.assertIn(self.need, returning_citizen.needs.all())
        self.assertIn(self.goal, returning_citizen.goals.all())

    def test_approval_model(self):
        approval = Approval.objects.create(
            returning_citizen=ReturningCitizen.objects.create(user=self.user),
            parole_officer=ParoleOfficer.objects.create(
                user=User.objects.create(username="parole_officer_user")
            ),
            approved=True,
        )

        self.assertTrue(
            approval.returning_citizen.care_team.parole_officers.filter(
                user=approval.parole_officer.user
            ).exists()
        )

    def test_questionnaire_str(self):
        self.assertEqual(str(self.questionnaire), "Test Questionnaire")

    def test_question_str(self):
        self.assertEqual(str(self.question), "Test Question")

    def test_user_response_str(self):
        self.assertEqual(
            str(self.user_response), "testuser's response to 'Test Question'"
        )


class AuthIntegrationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a test client
        self.client = Client()

    def test_login(self):
        # Simulate a login request
        response = self.client.post(
            "/accounts/login/", {"username": "testuser", "password": "testpassword"}
        )

        # Check if the login was successful (status code 200 or 302, depending on your setup)
        self.assertIn(response.status_code, [200, 302])

        # Check if the user is now logged in
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout(self):
        # Log in the user before testing logout
        self.client.login(username="testuser", password="testpassword")

        # Simulate a logout request
        response = self.client.post("/accounts/logout/")

        # Check if the logout was successful (status code 200 or 302, depending on your setup)
        self.assertIn(response.status_code, [200, 302])
        # Check if the user is now logged out
        self.assertNotIn("_auth_user_id", self.client.session)


class HomeViewTests(TestCase):
    def setUp(self):
        # Create test users and groups
        self.user_returning_citizen = User.objects.create_user(
            username="rc_user", password="testpass"
        )
        self.user_parole_officer = User.objects.create_user(
            username="po_user", password="testpass"
        )
        self.user_mentor = User.objects.create_user(
            username="mentor_user", password="testpass"
        )

        self.group_returning_citizen = Group.objects.create(
            name="Returning Citizen Role"
        )
        self.group_parole_officer = Group.objects.create(name="Parole Officer Role")
        self.group_mentor = Group.objects.create(name="Mentor Role")

        self.user_returning_citizen.groups.add(self.group_returning_citizen)
        self.user_parole_officer.groups.add(self.group_parole_officer)
        self.user_mentor.groups.add(self.group_mentor)

        # Create test model instances
        self.returning_citizen = ReturningCitizen.objects.create(
            user=self.user_returning_citizen
        )
        self.parole_officer = ParoleOfficer.objects.create(
            user=self.user_parole_officer
        )
        self.mentor = Mentor.objects.create(user=self.user_mentor)

    def test_authenticated_user_with_returning_citizen_role(self):
        self.client.login(username="rc_user", password="testpass")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Welcome")
        self.assertContains(response, "Returning Citizen")

    def test_authenticated_user_with_parole_officer_role(self):
        self.client.login(username="po_user", password="testpass")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Welcome")
        self.assertContains(response, "Parole Officer")

    def test_authenticated_user_with_mentor_role(self):
        self.client.login(username="mentor_user", password="testpass")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Welcome")
        self.assertContains(response, "Mentor")

    def test_unauthenticated_user(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)  # Redirect to login page


class DynamicQuestionnaireFormTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.user_rc = User.objects.create_user(
            username="testuser2", password="testpassword2"
        )

        # Create a questionnaire and questions for testing
        self.questionnaire = Questionnaire.objects.create(title="Test Questionnaire")
        self.question1 = Question.objects.create(
            questionnaire=self.questionnaire, text="Question 1", order=1
        )
        self.question2 = Question.objects.create(
            questionnaire=self.questionnaire, text="Question 2", order=2
        )

        # Add the user to the 'Returning Citizen Role' group
        returning_citizen_role, created = Group.objects.get_or_create(
            name="Returning Citizen Role"
        )
        mentor_role, created = Group.objects.get_or_create(name="Mentor Role")

        self.user_rc.groups.add(returning_citizen_role)
        self.user.groups.add(mentor_role)

        # Create a ReturningCitizen instance for self.user_rc
        self.returning_citizen_user_rc = ReturningCitizen.objects.create(
            user=self.user_rc,
            first_name="Value1",  # Adjust fields based on your model structure
            last_name="Value2",
        )
        care_team = self.returning_citizen_user_rc.care_team

        # Create a Mentor instance for self.user
        self.mentor_user = Mentor.objects.create(
            user=self.user,
            last_name="Mentor Last Name",
        )
        self.mentor_user.care_teams.add(care_team.id)

        # Get or create a CareTeam associated with the returning_citizen_user_rc

    def test_dynamic_questionnaire_form_submission(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

        # Create a dynamic form for the questionnaire
        DynamicQuestionnaireForm = create_dynamic_questionnaire_form(self.questionnaire)

        # Prepare POST data with responses
        post_data = {
            "care_team": self.returning_citizen_user_rc.care_team.id,
            f"question_{self.question1.id}": "Answer to question 1",
            f"question_{self.question2.id}": "Answer to question 2",
        }

        # Submit the form
        response = self.client.post(
            reverse("display_questionnaire", args=[self.questionnaire.id]), post_data
        )

        # Check if the form submission is successful and redirects to 'home'
        # self.assertRedirects(response, reverse('home'))

        # Check if the UserResponse objects are created in the database
        self.assertEqual(UserResponse.objects.count(), 2)

        # You can add more assertions based on your specific requirements

    def test_dynamic_questionnaire_form_display(self):
        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

        # Create a dynamic form for the questionnaire
        DynamicQuestionnaireForm = create_dynamic_questionnaire_form(self.questionnaire)

        # Access the questionnaire display page
        response = self.client.get(
            reverse("display_questionnaire", args=[self.questionnaire.id])
        )

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the form is in the response context
        self.assertIn("form", response.context)
