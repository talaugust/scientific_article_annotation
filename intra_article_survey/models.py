from django.db import models
from django_mysql.models import JSONField, ListTextField
from django.contrib.auth.models import User, Group
from annotationAPI.models import Article, Annotation, id_generator
from django.core.validators import MaxValueValidator
from multiselectfield import MultiSelectField


# common choices
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

EDU_CHOICES = [
    ('PRE-HIGH', 'Pre-high school'),
    ('HIGH', 'High school'),
    ('BACH', 'Bachelor\'s Degree'),
    ('MAST', 'Master\'s school'),
    ('DOCT', 'Doctorate (PhD)'),
]

STEM_CHOICES = [
    ('0', '0'),
    ('1-3', '1-3'),
    ('4-6', '4-6'),
    ('7-9', '7-9'),
    ('10+', '10+'),
]

TRUE_FALSE_CHOICES = [
    (0, 'None'),
    (1, 'Yes'),
    (2, 'No')
]

YES_NO_CHOICES = [
    ('0', 'No'),
    ('1', 'Yes'),
]

SCI_INFO_CHOICES = [
    ('MAGAZINES', 'Magazines (online or offline)'),
    ('NEWSPAPERS', 'Newspapers (online or offline)'),
    ('INTERNET', 'Internet'),
    ('PRINT', 'Book or other print'),
    ('TELEVISION', 'Television'),
    ('RADIO', 'Radio or podcast'),
    ('GOVERNMENT', 'Government agency'),
    ('FAMILY', 'Family'),
    ('FRIEND', 'Friend or colleague'),
    ('LIBRARY', 'Library'),
    ('REDDIT', 'Reddit'),
    ('OTHER', 'Other'),
]

SCI_INFO_TIME_CHOICES = [
    ('DAILY', 'Daily'),
    ('WEEKLY', 'Weekly'),
    ('MONTHLY', 'Monthly'),
    ('LESS', 'Less than monhtly'),
]




class Demographics(models.Model):

    # foriegn keys
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)

    # demographics
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    gender_self_describe = models.CharField(max_length=50, blank=True)
    english_prof = models.CharField(max_length=50, choices=PROF_CHOICES)
    education = models.CharField(max_length=50, choices=EDU_CHOICES)
    stem_background = models.CharField(max_length=50, choices=STEM_CHOICES)
    sci_info = MultiSelectField(choices=SCI_INFO_CHOICES)
    sci_info_time = models.CharField(max_length=50, choices=SCI_INFO_TIME_CHOICES)

    research_involved = models.CharField(max_length=10, choices=YES_NO_CHOICES, blank=False)

    profession = models.CharField(max_length=100, blank=True)

    # this is an odd thing to add, but for if we do it on turk, otherwise just won't use it
    HITid = models.CharField(max_length=25, blank=False, default=id_generator)


    # other
    # comments = models.TextField(blank=True)
    # agree_to_contact = models.BooleanField()


class ArticleResponse(models.Model):
	# foriegn keys
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(auto_now_add=True)

    enjoy = models.IntegerField(choices=LIKERT_CHOICES, default=0)

    is_most_interesting_highlight = models.BooleanField()

    int_why = models.TextField(blank=False)

    is_difficult_highlight = models.BooleanField()

    reactions = models.TextField(blank=True)

# for final questions
class GeneralEndQuestions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    sci_info_time_open = models.CharField(max_length=50, choices=SCI_INFO_TIME_CHOICES)
    open_comments = models.TextField(blank=True)




