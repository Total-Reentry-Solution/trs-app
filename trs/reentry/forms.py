from django import forms
from .models import UserResponse, Question, CareTeam, Mentor


class UserResponseForm(forms.ModelForm):
    care_team = forms.ModelChoiceField(
        queryset=CareTeam.objects.none(),
        label="Select Returning Citizen Care Team",
        required=True,
        empty_label="Select Returning Citizen Care Team Empty",
    )

    class Meta:
        model = UserResponse
        fields = []

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.pop("mentor_user", None)
        # print(user)

        # Limit the queryset based on the user's associated care teams
        if user is not None:
            mentor = Mentor.objects.get(user=user)
            self.fields["care_team"].queryset = mentor.care_teams.all()


def create_dynamic_questionnaire_form(questionnaire, user=None):
    """
    Dynamically create a form for the given questionnaire with fields for each question.
    """
    question_fields = {}
    questions = Question.objects.filter(questionnaire=questionnaire).order_by("order")

    for question in questions:
        field_name = f"question_{question.id}"
        question_fields[field_name] = forms.CharField(
            label=question.text, required=True, widget=forms.Textarea
        )

    # Add the care_team field to the dynamic form and pass the current user to the form if provided
    if user is not None:
        question_fields["care_team"] = forms.ModelChoiceField(
            queryset=user.mentor.care_teams.all(),
            label="Select Care Team",
            required=False,
            empty_label="Select Care Team",
        )

    DynamicQuestionnaireForm = type(
        "DynamicQuestionnaireForm", (UserResponseForm,), question_fields
    )
    return DynamicQuestionnaireForm
