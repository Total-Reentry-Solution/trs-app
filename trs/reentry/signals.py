from django.contrib.auth.signals import user_logged_in
from django.contrib import messages

def on_user_logged_in(sender, request, user, **kwargs):
    # Your message
    message = "Welcome! You have successfully logged in."

    # Add the message using messages.success
    messages.success(request, message)

# Connect the signal handler to the user_logged_in signal
user_logged_in.connect(on_user_logged_in)
