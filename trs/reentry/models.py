from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Approval(models.Model):
    returning_citizen = models.ForeignKey('ReturningCitizen', on_delete=models.CASCADE)
    parole_officer = models.ForeignKey('ParoleOfficer', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.returning_citizen.first_name + " " + self.returning_citizen.last_name + " <> " + self.parole_officer.user.username + " - Approved:  " + str(self.approved)

class CareTeam(models.Model):
    name = models.CharField(max_length=100)
    organization = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ParoleOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_teams = models.ManyToManyField(CareTeam, related_name="parole_officers", blank=True)
    organization = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)


@receiver(post_save, sender=ParoleOfficer)
def create_parole_officer_group(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Parole Officer Role')
        instance.user.groups.add(group)

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_teams = models.ManyToManyField(CareTeam, related_name="mentors", blank=True)
    organization = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)


@receiver(post_save, sender=Mentor)
def create_mentor_group(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='Mentor Role')
        instance.user.groups.add(group)

class Need(models.Model):
    need = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True)

    def __str__(self):
        return self.need

#possibly deprecated with Questionaire model and related models
class Goal(models.Model):
    goal = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True)

    def __str__(self):
        return self.goal

class QuestionnaireCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(QuestionnaireCategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text
    class Meta:
        ordering = ['order']

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()

    def category(self):
        return self.questionnaire.questionnaire_category

    def __str__(self):
        return f"{self.user.username}'s response to '{self.question.text}'"



class Address(models.Model):
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)



class ReturningCitizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    care_team = models.OneToOneField(CareTeam, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    needs = models.ManyToManyField(Need, blank=True)
    goals = models.ManyToManyField(Goal, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


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


@receiver(post_save, sender=Approval)
def add_parole_officer_to_care_team(sender, instance, created, **kwargs):
    if created and instance.approved:
        instance.returning_citizen.care_team.parole_officers.add(instance.parole_officer)
