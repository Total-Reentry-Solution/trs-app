from django import forms
from .models import UserResponse, Question

class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = []

def create_dynamic_questionnaire_form(questionnaire):
    """
    Dynamically create a form for the given questionnaire with fields for each question.
    """
    question_fields = {}
    questions = Question.objects.filter(questionnaire=questionnaire).order_by('order')

    for question in questions:
        field_name = f"question_{question.id}"
        question_fields[field_name] = forms.CharField(label=question.text, required=True)

    # Create a dynamic form class
    DynamicQuestionnaireForm = type('DynamicQuestionnaireForm', (UserResponseForm,), question_fields)

    return DynamicQuestionnaireForm
