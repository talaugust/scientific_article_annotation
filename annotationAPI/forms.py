from django.forms import ModelForm, Textarea, RadioSelect, HiddenInput, ChoiceField
from .models import AnnotationHIT, CommonHITinfo, AnnotationHITStories, AnnotationHITExplAna, AnnotationHITParagraph
from django.core.exceptions import ValidationError



################# NOT USING FOR UPWORK #################
# common form class for HITs
class CommonHITinfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        fields = [
            'age',
            'gender',
            'gender_self_describe',
            'english_prof',
            'agree_to_contact',
            'comments',
            ]
        widgets = {
            'comments': Textarea(attrs={'cols': 80, 'rows': 3}),
        }
        labels = {
            'age': 'What is your age?',
            'english_prof': 'How proficient are you in English?',
            'gender': 'What is your gender?',
            'gender_self_describe': 'Please self describe',
            'agree_to_contact': 'I agree to being contacted in the next few months about this HIT (this may involve additiona HITs).',
            'comments': 'Is there anything else about the study you would like to add?',
        }

################# NOT USING FOR UPWORK #################
# common form class for *additional* LITW form info 
class CommonLITWinfoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        fields = [
            'enjoy',
            'objective',
            # 'think_pressure',
            # 'force_opinion',
            ]
        widgets = {
            'enjoy': RadioSelect,
            'objective': RadioSelect,
            # 'think_pressure': RadioSelect,
            # 'force_opinion': RadioSelect,
        }
        labels = {
            'enjoy': 'The article was fun to read.',
            'objective': 'The article was objective.',
            # 'think_pressure': 'The article tried to pressure me to think a certain way.',
            # 'force_opinion': 'The article did not try to force its opinions on me.',
        }


class AnnotationHITForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lead_interest'].required = False # might break
        self.fields['is_main_points_highlight'].required = True
        self.fields['is_care_highlight'].required = True
        self.fields['is_story_highlight'].required = True
        self.fields['is_personal_highlight'].required = True
        self.fields['is_expl_highlight'].required = True
        self.fields['is_analogy_highlight'].required = True

        self.label = 'all'

    class Meta():
        model = AnnotationHIT
        fields =  ['is_lead',
         	'lead_interest',
          	'is_main_points_highlight',
           	'is_care_highlight',
            'is_conclusion',
            'is_story_highlight',
            'is_personal_highlight',
            'is_expl_highlight',
            'is_analogy_highlight',
            'comments',
            ]
        
        widgets = {
            'is_lead': RadioSelect,
            'is_conclusion': RadioSelect,
            'lead_interest': RadioSelect,
            'comments': Textarea(attrs={'cols': 80, 'rows': 3}),
        }
       
        labels = {
            'is_lead': 'Is there a lead? If so, please highlight the sentences that make up the lead and label it \'LEAD\' in the \'Comments...\' box that pops up.',
         	'lead_interest':'Independent of the topic, how excited does the lead make you about the rest of the article?',
          	'is_main_points_highlight': 'Check this box after highlighting the sentences with the main point(s) of the article with the label \'MAIN\'.',
           	'is_care_highlight': 'Did you highlight all sentences talking about the real world impact of the research with the label \'IMPACT\'?' ,
            'is_conclusion':'Is there a concluding sentence? If so, please highlight the sentences that make up this conclusion with the label \'CONCLUSION\'.' ,
            'is_story_highlight': 'Check this box after highlighting all storytelling sentences in the article with the label \'STORY\'.',
            'is_personal_highlight':'Check this box after highlighting all sentences in the article that describes personal details with the label \'PERSONAL\'.',
            'is_expl_highlight': 'Check this box after highlighting all explanations sentences in the article with the label \'EXPL\'.',
            'is_analogy_highlight':'Check this box after highlighting all sentences in the article with analogies with the label \'ANALOGY\'.',
       
        }

################# NOT USING FOR UPWORK #################
class AnnotationHITParagraphForm(CommonHITinfoForm, CommonLITWinfoForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lead_interest'].required = False # might break
        self.fields['is_main_points_highlight'].required = True
        self.fields['is_care_highlight'].required = True
        self.label = 'paragraph_specific'

    class Meta(CommonHITinfoForm.Meta, CommonLITWinfoForm.Meta):
        model = AnnotationHITParagraph
        fields = CommonHITinfoForm.Meta.fields + CommonLITWinfoForm.Meta.fields + ['is_lead',
            'lead_interest',
            'is_main_points_highlight',
            'is_care_highlight',
            'is_conclusion',
            ]
        widgets = CommonHITinfoForm.Meta.widgets
        widgets.update(CommonLITWinfoForm.Meta.widgets)
        widgets.update({
            'is_lead': RadioSelect,
            'is_conclusion': RadioSelect,
            'lead_interest': RadioSelect,
        })
        labels = CommonHITinfoForm.Meta.labels
        labels.update(CommonLITWinfoForm.Meta.labels)
        labels.update({
            'is_lead': 'Is there a lead? If so, please highlight the sentences that make up the lead and label it \'LEAD\' in the \'Comments...\' box that pops up.',
            'lead_interest':'Independent of the topic, how excited does the lead make you about the rest of the article?',
            'is_main_points_highlight': 'Check this box after highlighting the sentences with the main point(s) of the article with the label \'MAIN\'.',
            'is_care_highlight': 'Did you highlight all sentences talking about the real world impact of the research with the label \'IMPACT\'?' ,
            'is_conclusion':'Is there a concluding sentence? If so, please highlight the sentences that make up this conclusion with the label \'CONCLUSION\'.' ,
        
        })

################# NOT USING FOR UPWORK #################
class AnnotationHITStoriesForm(CommonHITinfoForm, CommonLITWinfoForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_story_highlight'].required = True
        self.fields['is_personal_highlight'].required = True
        self.label = 'personal_and_stories'

    class Meta(CommonHITinfoForm.Meta):
        model = AnnotationHITStories
        fields = CommonHITinfoForm.Meta.fields + ['is_story_highlight', 'is_personal_highlight']
        widgets = CommonHITinfoForm.Meta.widgets
        labels = CommonHITinfoForm.Meta.labels
        labels.update({
            'is_story_highlight': 'Check this box after highlighting all storytelling sentences in the article with the label \'STORY\'.',
            'is_personal_highlight':'Check this box after highlighting all sentences in the article that describes personal details with the label \'PERSONAL\'.',
        })

################# NOT USING FOR UPWORK #################
class AnnotationHITExplAnaForm(CommonHITinfoForm, CommonLITWinfoForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_expl_highlight'].required = True
        self.fields['is_analogy_highlight'].required = True
        self.label = 'explanation_and_analogies'

    class Meta(CommonHITinfoForm.Meta):
        model = AnnotationHITExplAna
        fields = CommonHITinfoForm.Meta.fields + ['is_expl_highlight', 'is_analogy_highlight']
        widgets = CommonHITinfoForm.Meta.widgets
        labels = CommonHITinfoForm.Meta.labels
        labels.update({
            'is_expl_highlight': 'Check this box after highlighting all explanations sentences in the article with the label \'EXPL\'.',
            'is_analogy_highlight':'Check this box after highlighting all sentences in the article with analogies with the label \'ANALOGY\'.',
        })


