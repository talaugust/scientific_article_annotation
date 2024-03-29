from django.forms import ModelForm, Textarea, RadioSelect, HiddenInput, ChoiceField, ValidationError
from .models import Participant, Definition, FluencyResponse, ComplexityResponse, FactualityResponse, Comment
import re 
from django.core.exceptions import ValidationError


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['age', 'english_prof', 'education', 'stem_exp',]
        labels = {
        	'age': 'What is your age?',
            'english_prof': 'How proficient are you in English?',
            'education': 'What is the highest level of education you have received or are currently pursuing?',
            'stem_exp': 'Approximately how many STEM courses have you taken after high school? (STEM stands for "science, technology, engineering, and math.")',
        }


class FluencyResponseForm(ModelForm):

    class Meta:
        model = FluencyResponse
        fields = ['fluency_rating', 'relevancy_rating']
        widgets = {
            'fluency_rating': RadioSelect,
            'relevancy_rating': RadioSelect,

        }
        # help_texts = {
        #     'fluency_rating': 'You cannot change your answer once you click submit.',
        #     'relevancy_rating': 'Please write a minimum of 10 characters.',

        # }
        labels = {
            'fluency_rating': 'How fluent is this definition?',
            'relevancy_rating': 'How relevant is this definition for the term?',
        }

class ComplexityResponseForm(ModelForm):

    class Meta:
        model = ComplexityResponse
        fields = ['complexity_rating', 'understand_rating']
        widgets = {
            'complexity_rating': RadioSelect,
            'understand_rating': RadioSelect,

        }
        help_texts = {
        	# 'complexity_rating': 'When rating definitions please focus on unfamiliar terms or very long, complicated sentences, not grammaticality.',
            'understand_rating': 'This includes the definition having terms that are unfamiliar to you.',

        }
        labels = {
            'complexity_rating': 'How complicated is the definition\'s text?',
            'understand_rating': 'Imagine you are looking up this term, how hard is it for you to understand this definition?',
        }

class FactualityResponseForm(ModelForm):

    class Meta:
        model = FactualityResponse
        fields = ['is_not_factual', 'factuality_rating']
        widgets = {
            'factuality_rating': RadioSelect,

        }
        help_texts = {
        	# 'complexity_rating': 'When rating definitions please focus on unfamiliar terms or very long, complicated sentences, not grammaticality.',
            'factuality_rating': 'If the definition is correct, just mark \'Not at all\' ',

        }
        labels = {
            'is_not_factual': 'Does this definition contain factually incorrect information?',
            'factuality_rating': 'If the definition contains factually incorrect information, how extensive are these errors?',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': Textarea(attrs={'cols': 40, 'rows': 3}),

        }
        labels = {
            'comment_text': 'Anything else you would like to add?',
        }
