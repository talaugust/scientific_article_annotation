from django.db import models
from django_mysql.models import JSONField, ListTextField
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator
from django.db.models import Count, Q
import uuid
import string
import random


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
TRUE_FALSE_CHOICES = [
    (0, 'None'),
    (1, 'Yes'),
    (2, 'No')
]


# from: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
# for generating hit code
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ArticleManager(models.Manager):
    def isHITAvaliable(self):
        articles = []
        HITableArticles = super().get_queryset().filter(HITable=True).annotate(number_of_HITs=Count('annotationhit'))
        return HITableArticles.filter(number_of_HITs__lt=2)

    def getUserAnnotated(self, user, order=None):
        user_annotations = Count('annotation', filter=Q(annotation__user_id=user.id))
        avalaibleArticles = super().get_queryset().annotate(user_annotations=user_annotations)
        if order is not None:
            return avalaibleArticles.filter(user_annotations__gt=0).order_by(order)
        else:
            return avalaibleArticles.filter(user_annotations__gt=0).order_by('-updated')

    # same as above but for unannotated articles
    def getNotUserAnnotated(self, user, order=None):
        user_annotations = Count('annotation', filter=Q(annotation__user_id=user.id))
        avalaibleArticles = super().get_queryset().annotate(user_annotations=user_annotations)
        if order is not None:
            return avalaibleArticles.filter(user_annotations=0).order_by(order)
        else:
            return avalaibleArticles.filter(user_annotations=0).order_by('-updated')

    def getNoneAnnotated(self, order=None):
        avalaibleArticles = super().get_queryset().annotate(number_of_HITs=Count('annotationhit'))
        if order is not None:
            return avalaibleArticles.filter(number_of_HITs=0).order_by(order)
        else:
            return avalaibleArticles.filter(number_of_HITs=0)




class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    title = models.TextField()
    uri = models.URLField()
    lead = models.TextField(blank=True)
    site = models.TextField()
    HITable = models.BooleanField(default=False)
    objects = ArticleManager()


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

################# NOT USING FOR UPWORK #################
# abstract model class for HIT form
# using it for different annotation hits we could want 
class CommonHITinfo(models.Model):

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

     # demographics
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    gender_self_describe = models.CharField(max_length=50, blank=True)
    english_prof = models.CharField(max_length=50, choices=PROF_CHOICES)

    # other
    comments = models.TextField(blank=True)
    agree_to_contact = models.BooleanField()

    # this field is hidden until everything is submitted
    HITid = models.CharField(max_length=25, blank=False, default=id_generator)

    class Meta:
        abstract = True

################# NOT USING FOR UPWORK #################
# abstract model class for *additional* LITW form info 
class CommonLITWinfo(models.Model):

    enjoy = models.IntegerField(choices=LIKERT_CHOICES, default=0)
    objective = models.IntegerField(choices=LIKERT_CHOICES, default=0)
    # think_pressure = models.IntegerField(choices=LIKERT_CHOICES, default=0, blank=True)
    # force_opinion = models.IntegerField(choices=LIKERT_CHOICES, default=0, blank=True)

    class Meta:
        abstract = True



# For upwork really only using this
class AnnotationHIT(models.Model):
    
    is_lead = models.IntegerField(choices=TRUE_FALSE_CHOICES, default=0)
    lead_interest =  models.IntegerField(choices=LIKERT_CHOICES, default=0)
    is_main_points_highlight = models.BooleanField()
    is_care_highlight = models.BooleanField(blank=False)
    is_conclusion = models.IntegerField(choices=TRUE_FALSE_CHOICES, default=0)
    is_story_highlight = models.BooleanField()
    is_personal_highlight = models.BooleanField()
    is_expl_highlight = models.BooleanField()
    is_analogy_highlight = models.BooleanField()

    ################# ADDED HERE FROM CommonHITinfo #################
    comments = models.TextField(blank=True)

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

################# NOT USING FOR UPWORK #################
class AnnotationHITParagraph(CommonHITinfo, CommonLITWinfo):
    
    is_lead = models.IntegerField(choices=TRUE_FALSE_CHOICES, default=0)
    lead_interest =  models.IntegerField(choices=LIKERT_CHOICES, default=0)
    is_main_points_highlight = models.BooleanField()
    is_care_highlight = models.BooleanField(blank=False)
    is_conclusion = models.IntegerField(choices=TRUE_FALSE_CHOICES, default=0)


################# NOT USING FOR UPWORK #################
# for including stories and personal details
class AnnotationHITStories(CommonHITinfo, CommonLITWinfo):
    is_story_highlight = models.BooleanField()
    is_personal_highlight = models.BooleanField()
    

################# NOT USING FOR UPWORK #################
# for including stories and personal details
class AnnotationHITExplAna(CommonHITinfo, CommonLITWinfo):
    is_expl_highlight = models.BooleanField()
    is_analogy_highlight = models.BooleanField()






