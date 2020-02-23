from django.forms import ModelForm, Textarea, RadioSelect, HiddenInput, ChoiceField
from .models import AnnotationHIT
from django.core.exceptions import ValidationError



class AnnotationHITForm(ModelForm):
    class Meta:
        model = AnnotationHIT
        fields = ['is_lead',
         	'lead_interest',
          	'is_main_points_highlight',
           	'is_care_highlight',
            'is_conclusion',
            'age',
            'gender',
            'gender_self_describe',
            'english_prof',
            'comments']
        widgets = {
        	'is_lead': RadioSelect,
        	'is_conclusion': RadioSelect,
         	'lead_interest': RadioSelect,
            'comments': Textarea(attrs={'cols': 80, 'rows': 3})
        }
        labels = {
            'is_lead': 'Is there a lead? If so, please highlight the sentences that make up the lead',
         	'lead_interest':'Please highlight the lead and rate, on a scale from 1-5, 1 being not at all and 5 being extremely, how excited the lead made about the rest of the article?',
          	'is_main_points_highlight': 'Check this box after highlighting the sentences with the main point(s) of the article	 ',
           	'is_care_highlight': 'Did you highlight all \'Why should I care?\' sentences?' ,
            'is_conclusion':'Is there a concluding sentence? If so, please highlight the sentences that make up this conclusion' ,
            'age': 'What is your age?',
            'english_prof': 'How proficient are you in English?',
            'gender': 'What is your gender?',
            'gender_self_describe': 'Please self describe',
            'comments': 'Is there anything else about the study you would like to add?'

        }