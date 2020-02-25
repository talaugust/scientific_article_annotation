from django.db import models
from django_mysql.models import JSONField, ListTextField
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator
import uuid


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    title = models.TextField()
    uri = models.URLField()
    lead = models.TextField(blank=True)
    site = models.TextField()

class Annotation(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)
    quote = models.TextField(blank=False)
    permissions = JSONField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    ranges = JSONField()
    tags = JSONField(blank=True)
    uri = models.URLField()
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )

# model for HIT form
class AnnotationHIT(models.Model):
    LIKERT_CHOICES = [
        (0, 'None'),
        (1, ''),
        (2, ''),
        (3, ''),
        (4, ''),
        (5, ''),
        (6, ''),
        (7, ''),
    ]
    GENDER_CHOICES = [
        ('MALE', 'male'),
        ('FEMALE', 'female'),
        ('NON-BIN', 'non-binary'),
        ('SELF-DESCR', 'prefer to self-describe'),
        ('NOT_SAY', 'prefer not to say'),
    ]
    PROF_CHOICES = [
        ('ELEM', 'Elementary Proficiency'),
        ('LIMIT', 'Limited Working Proficiency'),
        ('PROF', 'Professional Working Proficiency'),
        ('FULL', 'Full Professional Proficiency'),
        ('NATIVE', 'Native / Bilingual '),
    ]
    TRUE_FALSE_CHOICES = [
        (0, 'None'),
        (1, 'Yes'),
        (2, 'No')
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    is_lead = models.IntegerField(choices=TRUE_FALSE_CHOICES, default=0)
    lead_interest =  models.IntegerField(choices=LIKERT_CHOICES, default='None')
    is_main_points_highlight = models.BooleanField()
    is_care_highlight = models.BooleanField(blank=False)
    is_conclusion = models.IntegerField(choices=TRUE_FALSE_CHOICES, default=0)

    # demographics
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    gender_self_describe = models.CharField(max_length=50, blank=True)
    english_prof = models.CharField(max_length=50, choices=PROF_CHOICES)

    # other
    comments = models.TextField(blank=True)
    agree_to_contact = models.BooleanField()





