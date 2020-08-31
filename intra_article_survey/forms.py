from django import forms
from .models import Demographics, ArticleResponse
from django.forms import ModelForm, RadioSelect, Textarea

class DemographicsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Demographics
        fields = ['age', 'gender', 'gender_self_describe', 'english_prof', 'education', 'stem_background', 'sci_info', 'profession']
        # widgets = {
  #       }

        labels = {
            'age': 'What is your age?',
            'gender': 'What is your gender?',
            'gender_self_describe': 'Please self-describe your gender.',
            'english_prof': 'What is your English proficeancy?',
            'education':'What is the highest level of education you have received or are currently pursuing?', 
            'stem_background': 'Approximately how many STEM courses have you taken after high school? (STEM stands for "science, technology, engineering, and math.")',
            'sci_info': 'Where do you get most of your information about science and technology? Check all that apply',
            'profession': 'What is your profession?'
        }


class ArticleResponseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_most_interesting_highlight'].required = True

    class Meta:
        model = ArticleResponse
        fields = ['enjoy', 'is_most_interesting_highlight', 'is_difficult_highlight', 'reactions']
        widgets = {
            'enjoy': RadioSelect,
            'reactions': Textarea(attrs={'cols': 80, 'rows': 3}),

        }

        labels = {
            'enjoy': 'How much did you enjoy the article you just read?',
            'is_most_interesting_highlight': 'I have highlighted the most interesting sentences to me.',
            'is_difficult_highlight': 'I have highlighted any difficult sentences.',
            'reactions': 'Do you have any other thoughts or reactions to the article that you would like to share?',   
        }