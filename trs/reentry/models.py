from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class CareTeam(models.Model):
    name = models.CharField(max_length=100)
    organization = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ParoleOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_teams = models.ManyToManyField(CareTeam, related_name="parole_officers", blank=True)
    organization = models.CharField(max_length=100)

@receiver(post_save, sender=ParoleOfficer)
def create_parole_officer_group(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Parole Officer Role')
        instance.user.groups.add(group)

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_teams = models.ManyToManyField(CareTeam, related_name="mentors", blank=True)
    organization = models.CharField(max_length=100)

@receiver(post_save, sender=Mentor)
def create_mentor_group(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Mentor Role')
        instance.user.groups.add(group)

class ReturningCitizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_team = models.OneToOneField(CareTeam, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


    def save(self, *args, **kwargs):
        # If a care team does not exist, create one and associate it with the user
        if not self.care_team:
            care_team = CareTeam.objects.create(name=f"Care Team for {self.first_name} {self.last_name}")
            self.care_team = care_team
        super().save(*args, **kwargs)

@receiver(post_save, sender=ReturningCitizen)
def create_returning_citizen_group(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Returning Citizen Role')
        instance.user.groups.add(group)
