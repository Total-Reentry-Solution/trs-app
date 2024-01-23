from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test, login_required
from reentry.models import (
    ReturningCitizen,
    Mentor,
    ParoleOfficer,
    Questionnaire,
    Question,
    UserResponse,
)
from reentry.forms import create_dynamic_questionnaire_form


def get_model_for_group(user):
    # Define your group-to-model and template mapping here
    group_mapping = {
        "Returning Citizen Role": {"model": ReturningCitizen},
        "Parole Officer Role": {"model": ParoleOfficer},
        "Mentor Role": {"model": Mentor},
    }

    # Get user's groups
    user_groups = user.groups.values_list("name", flat=True)

    # Find the first matching group mapping for the user's groups
    for group in user_groups:
        if group in group_mapping:
            return group_mapping[group]

    return None


def is_mentor(user):
    """
    Check if the user has only the "Mentor Role" group.
    """
    return (
        user.is_authenticated
        and user.groups.filter(name="Mentor Role").exists()
    )


mentor_required = user_passes_test(is_mentor, login_url="home")


def get_mentor_care_teams(user):
    # Check if the user is a Mentor
    try:
        mentor = Mentor.objects.get(user=user)
    except Mentor.DoesNotExist:
        # Handle the case when the user is not a Mentor
        return {"error": "Not a Mentor"}

    # Retrieve the associated CareTeams
    care_teams = mentor.care_teams.all()

    # Retrieve and include the ReturningCitizen user's first and last name
    care_teams_data = []
    for team in care_teams:
        # Assuming there is a ForeignKey relationship from CareTeam to ReturningCitizen
        returning_citizen_user = team.returningcitizen if team.returningcitizen else None

        care_team_info = {
            "name": team.name,
            "returning_citizen_name": f"{returning_citizen_user.first_name} {returning_citizen_user.last_name}" if returning_citizen_user else None
        }

        care_teams_data.append(care_team_info)
    # Return the CareTeams data as a dictionary
    return {"care_teams": care_teams_data}

@login_required 
@user_passes_test(lambda u: get_model_for_group(u) is not None, login_url=None)
def home(request):
    group_mapping = get_model_for_group(request.user)

    try:
        model_instance = group_mapping["model"].objects.get(user=request.user)
        model_name = group_mapping["model"].__name__.lower()

        if model_name == "mentor":
            # Call the function to get mentor care teams data
            mentor_care_teams_data = get_mentor_care_teams(request.user)
            #print(mentor_care_teams_data)
            return render(
                request,
                "home.html",
                {
                    "model_instance": model_instance,
                    "model_name": model_name,
                    "mentor_care_teams_data": mentor_care_teams_data,
                },
            )

        return render(
            request,
            "home.html",
            {"model_instance": model_instance, "model_name": model_name},
        )
    except group_mapping["model"].DoesNotExist:
        return HttpResponseForbidden(
            f"You do not have a {group_mapping['model'].__name__} profile."
        )


@login_required
@mentor_required
def display_questionnaire(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)

    # Create a dynamic form for the questionnaire
    DynamicQuestionnaireForm = create_dynamic_questionnaire_form(
        questionnaire, user=request.user
    )

    if request.method == "POST":
        form = DynamicQuestionnaireForm(request.POST)
        if form.is_valid():
            for question in questionnaire.question_set.all():
                response_field_name = f"question_{question.id}"

                # Get the selected care_team value from the form
                selected_care_team = form.cleaned_data["care_team"]

                # Assuming ReturningCitizen model has a ForeignKey relationship with CareTeam
                returning_citizen_user = selected_care_team.returningcitizen.user

                user_response = UserResponse(
                    user=returning_citizen_user,
                    questionnaire=questionnaire,
                    question=question,
                    response=form.cleaned_data[response_field_name],
                    submitted_by=request.user,
                )
                user_response.save()

            # Redirect to the next page or thank-you page
            return redirect("home")
    else:
        form = DynamicQuestionnaireForm()

    return render(
        request,
        "display_questionnaire.html",
        {"form": form, "questionnaire": questionnaire},
    )
