from django.db import models
from django_mysql.models import JSONField, ListTextField
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db.models import Count, Q
import uuid
import string
import random

# Create your models here.


# from: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
# for generating hit code
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def uuid_int():
    return uuid.uuid4().int

# # TODO: ADD MORE LATER
# MODEL_CHOICES = [
#     ('SVM-NEWS', 'SVM reranker for news text'),
#     ('SVM-JOURNAL', 'SVM reranker for academic text'),
# ]

MODEL_CHOICES = [
    # ('BERT-RERANK-JOURNAL', 'BERT Reranker Journal'),
    # ('BERT-RERANK-NEWS', 'BERT Reranker News'),
    ('SVM-RERANK-JOURNAL', 'SVM Reranker Journal'),
    ('SVM-RERANK-NEWS', 'SVM Reranker News'),
    ('GEDI-NEWS', 'Gedi News'),
    ('GEDI-JOURNAL', 'Gedi Journal'),
    ('DEXPERT-JOURNAL','DExpert Journal'),
    ('DEXPERT-NEWS', 'DExpert News'),
    # ('DAPT-NEWS', 'DAPT News'),
    # ('DAPT-JOURNAL', 'DAPT Journal'),
]

# common choices
LIKERT_CHOICES = [
    (0, 'None'),
    (1, 'Not at all'),
    (2, ''),
    (3, ''),
    (4, 'Very'),
]


# from participant classes in expert_turing
class Participant(models.Model):

    ''' 
    A participant model. Includes:
        (1) any demographics
        (2) a user
        (3) definition assignments: which definitions that user will be evaluating
        (4) eval assignment: if it is fluency or complexity

    '''

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

    EVAL_CHOICES = [
        ('FLUENCY', 'Fluency'),
        ('COMPLEX', 'Complexity'),
    ]

    EDU_CHOICES = [
        ('PRE-HIGH', 'Pre-high school'),
        ('HIGH', 'High school'),
        ('COLLEGE', 'College'),
        ('GRAD', 'Graduate school'),
        ('PROFESSION', 'Profession school'),
    ]

    STEM_CHOICES = [
        ('0', '0'),
        ('1-3', '1-3'),
        ('4-6', '4-6'),
        ('7-9', '7-9'),
        ('10+', '10+'),
    ]



    # demographics:
    # age = models.PositiveIntegerField(validators=[MaxValueValidator(150), MinValueValidator(18)])
    # gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    # gender_self_describe = models.CharField(max_length=50, blank=True)
    
    english_prof = models.CharField(max_length=50, choices=PROF_CHOICES)
    education = models.CharField(max_length=50, choices=EDU_CHOICES)
    stem_exp = models.CharField(max_length=50, choices=STEM_CHOICES)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(150), MinValueValidator(18)])

    eval_exp = models.CharField(max_length=50, choices=EVAL_CHOICES)
    order = models.TextField(blank=False) # TODO: potentially add a method for establishing order here
    
    created = models.DateTimeField(default=now)
    HITid = models.CharField(max_length=25, blank=False, default=id_generator)



# making a term class to more easily organize the responses


class TermManager(models.Manager):
    # returns n terms, randomly selected will throw an error if sampling more than the population
    def getRandomTerms(self, n):

        # get all the ids of the qs in a list
        all_ids = list(super().get_queryset().values_list('id', flat=True))  

        # randomly sample n of them (without replacement)
        random_sample_ids = random.sample(all_ids, n)

        # return, with an extra shuffle just in case
        return super().get_queryset().filter(pk__in=random_sample_ids).order_by('?')

    # returns n terms, randomly selected that have AT LEAST one definition with < k TOTAL complexity responses
    def getRandomComplexityNotAnnotatedTerms(self, n, k):

        # first annotate the terms for their total number of complexity responses
        avalaibleTerms = super().get_queryset().annotate(number_complexity_responses=Count('definition__complexityresponse'))

        # while this doesn't look at individual definitions, the assumption is that if the definition 
        # manager restricts each definition to at most 2 complexity responses, then we can just use 
        # an aggregate filter here (of 6*2 = 12 = k)
        avalaibleTerms = avalaibleTerms.filter(number_complexity_responses__lte=k)

        # get all the ids of the qs in a list
        all_avaliable_ids = list(avalaibleTerms.values_list('id', flat=True))  

        # randomly sample n of them (without replacement)
        random_sample_ids = random.sample(all_avaliable_ids, n)

        # return, with an extra shuffle just in case
        return avalaibleTerms.filter(pk__in=random_sample_ids).order_by('?')

class Term(models.Model):
    TERM_CATEGORIES = [
            ('WIKI', 'Wikipedia'),
            ('MEDQUAD', 'MedQuad'),
        ]

    term_text = models.CharField(max_length=100, blank=False)
    category = models.CharField(max_length=15, choices=TERM_CATEGORIES, blank=False)
    objects = TermManager()


class DefinitionManager(models.Manager):

    # function for getting all definitions with less than n responses
    # TODO: One issue with these sorts of checks is that it risks returning an empty qset. 
    # this is mostly ok since we will populate the db prior to deploying, and will only deploy the 
    # number of hits that will fill out the db, but still a good thing to know. 
    # also order_by is super slow, but whatever

    # returns n definitions randomly except none are from the same term and we cover all generator types
    
    def getRandomDefs(self, n, testing=False):

        # first off get a random set of unique terms
        terms = Term.objects.getRandomTerms(n)

        def_pks = set()
        generator_choices = [x[0] for x in MODEL_CHOICES]

        # randomize here so we can pop later
        random.shuffle(generator_choices)

        # for each term, select a random model definition from a model that hasn't already been selected
        for t in  terms:
            # get all the definitions for this term
            defs = super().get_queryset().filter(term=t) 
            # make sure there are still some models left
            if len(generator_choices) > 0:
                # select a random model to get a definition from
                model = generator_choices.pop()
                def_pks.add(defs.filter(model_type=model).first().pk)
            else:
                # else just pick a random model
                def_pks.add(defs.order_by('?').first().pk)

        return super().get_queryset().filter(pk__in=def_pks).order_by('?')

    # returns n definitions that have not been responded to by more than 2 people (for complexity response) 
    def getAvaliableComplexityDefs(self, n, max_num_complexity_responses=2):

        # first off get a random set of unique terms
        terms = Term.objects.getRandomComplexityNotAnnotatedTerms(n, k=max_num_complexity_responses*len(MODEL_CHOICES))

        def_pks = set()

        # for each term, select definition that has less than 2 complexity responses
        for t in terms:
            defs = super().get_queryset().filter(term=t).annotate(number_complexity_responses=Count('complexityresponse'))
            defs = defs.filter(number_complexity_responses__lte=max_num_complexity_responses) 
            def_pks.add(defs.order_by('?').first().pk)

        return super().get_queryset().filter(pk__in=def_pks).order_by('?')

    # not currently using
    def getNotParticipantAnnotated(self, participant_id, responseType):
        participant_ratings = Count('annotation', filter=Q(responseType__participant_id=participant_id))
        avalaibleDefinitions = super().get_queryset().annotate(participant_ratings=participant_ratings)
        return avalaibleArticles.filter(user_annotations=0).order_by('?')
        

class Definition(models.Model):

    '''
    A definition model. Includes:
        (1) the generated definition text
        (2) the model (including the complexity aim)
        (3) the term being defined
        (4) the category of the term
        (5) a context sentence that uses the term 

    '''


    # participant = models.ForeignKey(
    #     Participant,
    #     on_delete=models.CASCADE,
    # )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    term = models.ForeignKey(
        Term,
        on_delete=models.CASCADE,
    )

    def_text = models.TextField(blank=False)
    model_type = models.CharField(max_length=100, choices=MODEL_CHOICES, blank=False)
    context_sentence = models.TextField(blank=True)
    reference = models.TextField(blank=True)
    objects = DefinitionManager()

class FluencyResponse(models.Model):
    '''
    A fluency response model. Includes:
        (1) the definition
        (2) the participant
        (3) the fluency score
        (4) the relevance score
        (5) a timestamp
    '''
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
    )
    definition = models.ForeignKey(
        Definition,
        on_delete=models.CASCADE,
    )

    created = models.DateTimeField(default=now)

    fluency_rating = models.IntegerField(choices=LIKERT_CHOICES, default=0)
    relevancy_rating = models.IntegerField(choices=LIKERT_CHOICES, default=0)


class ComplexityResponse(models.Model):
    '''
    A complexity response model. Includes:
        (1) the definition
        (2) the participant
        (3) the complexity score
        (4) (?) another complexity score based on understandability
        (5) a timestamp
    '''


    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
    )
    definition = models.ForeignKey(
        Definition,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(default=now)
    complexity_rating = models.IntegerField(choices=LIKERT_CHOICES, default=0)
    understand_rating = models.IntegerField(choices=LIKERT_CHOICES, default=0)



class Comment(models.Model):
    participant = models.ForeignKey(
        'Participant',
        on_delete=models.CASCADE,
    )
    
    comment_text = models.TextField(blank=True)
