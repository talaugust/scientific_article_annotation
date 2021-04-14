from django.forms import ModelForm, Textarea, RadioSelect, HiddenInput, ChoiceField, ValidationError
from .models import Participant, Definition, FluencyResponse, Comment
import re 
from django.core.exceptions import ValidationError


class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['english_prof', 'education', 'stem_exp',]
        labels = {
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
