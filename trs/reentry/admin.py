from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from reentry.models import ParoleOfficer, Mentor, CareTeam, ReturningCitizen, Approval, Need, Goal, Address


# Define an inline admin descriptor for mmodel
# which acts a bit like a singleton
class ParoleOfficerInline(admin.StackedInline):
    model = ParoleOfficer
    can_delete = False
    verbose_name_plural = "parole officer"

class MentorInline(admin.StackedInline):
    model = Mentor
    can_delete = False
    verbose_name_plural = "mentor"

class ReturningCitizenInline(admin.StackedInline):
    model = ReturningCitizen
    can_delete = False
    verbose_name_plural = "returning citizen"

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ParoleOfficerInline, MentorInline, ReturningCitizenInline]

admin.site.register(CareTeam)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Approval)
admin.site.register(Need)
admin.site.register(Goal)
