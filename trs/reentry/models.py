from django.db import models
from django.contrib.auth.models import User

class CareTeam(models.Model):
    name = models.CharField(max_length=100)
    organization = models.TextField(null=True, blank=True)

class ParoleOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_teams = models.ManyToManyField(CareTeam, related_name="careteams", blank=True)
    organization = models.CharField(max_length=100)

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_teams = models.ManyToManyField(CareTeam, blank=True)
    organization = models.CharField(max_length=100)

class ReturningCitizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_teams = models.ManyToManyField(CareTeam, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
