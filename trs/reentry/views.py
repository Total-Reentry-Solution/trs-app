# from django.shortcuts import render
# from django.http import HttpResponseForbidden
# from django.contrib.auth.decorators import user_passes_test
# from reentry.models import ReturningCitizen, Mentor, ParoleOfficer

# def get_model_and_template_for_group(user):
#     # Define your group-to-model and template mapping here
#     group_mapping = {
#         'Returning Citizen Role': {'model': ReturningCitizen, 'template': 'rc_landing.html'},
#         'Parole Officer Role': {'model': ParoleOfficer, 'template': 'po_landing.html'},
#         'Mentor Role': {'model': Mentor, 'template': 'mentor_landing.html'},
#         # Add more mappings as needed
#     }
    
#     # Get user's groups
#     user_groups = user.groups.values_list('name', flat=True)

#     # Find the first matching group mapping for the user's groups
#     for group in user_groups:
#         if group in group_mapping:
#             return group_mapping[group]

#     return None

# @user_passes_test(lambda u: get_model_and_template_for_group(u) is not None, login_url=None)
# def home(request):
#     group_mapping = get_model_and_template_for_group(request.user)

#     try:
#         model_instance = group_mapping['model'].objects.get(user=request.user)
#         #template_name = group_mapping['template']
#         return render(request, "home.html", {'model_instance': model_instance})
#     except group_mapping['model'].DoesNotExist:
#         return HttpResponseForbidden(f"You do not have a {group_mapping['model'].__name__} profile.")



from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from reentry.models import ReturningCitizen, Mentor, ParoleOfficer

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

@user_passes_test(lambda u: get_model_for_group(u) is not None, login_url=None)
def home(request):
    group_mapping = get_model_for_group(request.user)

    try:
        model_instance = group_mapping['model'].objects.get(user=request.user)
        #template_name = group_mapping['template']

        # Create a variable with the model name to pass to the template
        model_name = group_mapping['model'].__name__.lower()
        print(model_name)
        print(model_instance)
        return render(request, "home.html", {'model_instance': model_instance, 'model_name': model_name})
    except group_mapping['model'].DoesNotExist:
        return HttpResponseForbidden(f"You do not have a {group_mapping['model'].__name__} profile.")
