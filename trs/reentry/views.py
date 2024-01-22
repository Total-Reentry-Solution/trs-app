from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test, login_required
from reentry.models import ReturningCitizen, Mentor, ParoleOfficer, Questionnaire, Question, UserResponse
from reentry.forms import create_dynamic_questionnaire_form

def get_model_for_group(user):
    # Define your group-to-model and template mapping here
    group_mapping = {
        'Returning Citizen Role': {'model': ReturningCitizen},
        'Parole Officer Role': {'model': ParoleOfficer},
        'Mentor Role': {'model': Mentor},

    }
    
    # Get user's groups
    user_groups = user.groups.values_list('name', flat=True)

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
        user.is_authenticated and
        user.groups.filter(name='Mentor Role').exists() and
        user.groups.count() == 1  # Ensure the user has only the specified group
    )

mentor_required = user_passes_test(is_mentor, login_url='home')


@login_required
@user_passes_test(lambda u: get_model_for_group(u) is not None, login_url=None)
def home(request):
    group_mapping = get_model_for_group(request.user)

    try:
        model_instance = group_mapping['model'].objects.get(user=request.user)
        #template_name = group_mapping['template']

        # Create a variable with the model name to pass to the template
        model_name = group_mapping['model'].__name__.lower()
        return render(request, "home.html", {'model_instance': model_instance, 'model_name': model_name})
    except group_mapping['model'].DoesNotExist:
        return HttpResponseForbidden(f"You do not have a {group_mapping['model'].__name__} profile.")

@login_required
@mentor_required
def display_questionnaire(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)

    # Create a dynamic form for the questionnaire
    DynamicQuestionnaireForm = create_dynamic_questionnaire_form(questionnaire, user=request.user)

    if request.method == 'POST':
        form = DynamicQuestionnaireForm(request.POST)
        if form.is_valid():
            for question in questionnaire.question_set.all():
                response_field_name = f"question_{question.id}"

                # Get the selected care_team value from the form
                selected_care_team = form.cleaned_data['care_team']

                # Assuming ReturningCitizen model has a ForeignKey relationship with CareTeam
                returning_citizen_user = selected_care_team.returningcitizen.user

                user_response = UserResponse(
                    user=returning_citizen_user,
                    questionnaire=questionnaire,
                    question=question,
                    response=form.cleaned_data[response_field_name],
                    submitted_by=request.user
                )
                user_response.save()

            # Redirect to the next page or thank-you page
            return redirect('home')
    else:
        form = DynamicQuestionnaireForm()

    return render(request, 'display_questionnaire.html', {'form': form, 'questionnaire': questionnaire})
