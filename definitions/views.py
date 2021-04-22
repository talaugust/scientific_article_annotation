from django.shortcuts import render, redirect, reverse
from annotationAPI.models import Annotation, Article
from .models import Participant, Definition, FluencyResponse, ComplexityResponse, Comment
from .forms import ParticipantForm, FluencyResponseForm, ComplexityResponseForm, CommentForm
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views import View
import uuid
import random
from article_annotation.settings import DEBUG


TESTING = False  
IS_SINGLE_PARTICIPANT = True
TEST_DATA_DEM = {'english_prof': 'LIMIT', 'education': 'PRE-HIGH', 'stem_exp': '1-3'}
TEST_DATA_RESPONSE = {'fluency_rating': 4, 'relevancy_rating': 4}

RESPONSE_MAP = {1: 'FLUENCY', 2:'COMPLEXITY'}
RESPONSE_TYPE_MAP = {'FLUENCY': FluencyResponse, 'COMPLEXITY':ComplexityResponse}

DEF_COUNT = 3

# Create your views here.
def landing(request, response_type=None):

    # TODO: make sure this is taken out
        # if TESTING:
    request.session.flush() 

    # way of specifying which response type we want, fluency or complexity
    response_type = RESPONSE_MAP.get(response_type, None)

    # if it is none, pick randomly 
    if response_type is None:
        request.session['response_type'] = random.choice(list(RESPONSE_MAP.values()))
    else:
        request.session['response_type'] = response_type


    return render(request, 'definitions/landing.html', {})


def DefinitionInstructions(request):

    context = {}

    print('HERE')

    def_count = request.session.get('defCount')
    def_ids = request.session.get('defIDs')


    context['response_type'] = request.session.get('response_type')

    context.update({'pk': def_ids[def_count - 1]})
    
    return render(request, 'definitions/instructions.html', context)



# helper function for detecting if a participant already has filled out a particular response for a given definition
def get_definitionresponse_participant(request, definition, responseType):
    participant_id = request.session.get('participantID')


    if definition is None:
        def_responses = responseType.objects.filter(participant_id=participant_id)
    else:
        def_responses = responseType.objects.filter(participant_id=participant_id, definition_id=definition.id)

    # while there should only be one response per snippet and participant, would rather not break
    # if there are multiple, so just return the first if that is the case
    if len(def_responses) == 0:
        return None
    return def_responses.first()  

'''
Demographics
'''

class DefinitionDemographicsView(FormView):

    template_name = 'definitions/demographics.html'
    form_class = ParticipantForm
    model = Participant


    def set_order(self):

        
        # if this is a single participant set up, get all the definitions instead
        # this will only be called the first time the participant fills out the demographics, 
        if IS_SINGLE_PARTICIPANT:
             # get all the definitions
            defs = Definition.objects.all()
        else:
            defs = Definition.objects.getRandomDefs(DEF_COUNT, testing=TESTING)
        
        def_ids = [str(d.id) for d in defs]

        # save the def ids
        self.request.session['defIDs'] = def_ids

        # set current def number
        self.request.session['defCount'] = 1

        # set max number
        self.request.session['maxDefCount'] = len(def_ids)

        return def_ids


    # overriding to add in testing infrastructure
    def get_context_data(self, **kwargs):
        
        if TESTING:
            context = super().get_context_data(**kwargs)
            context['form'] = self.form_class(initial=TEST_DATA_DEM)
            return context
        
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):  
        # check if a session already exists for this participant and we are assuming a single participant
        if IS_SINGLE_PARTICIPANT:
            participant_id = self.request.session.get('participantID', None)

            print(participant_id)

            # first time this participant is logging on
            if participant_id is None:
                return super().get(request, *args, **kwargs)

            # the participant exists, allow them to resume rating (note that the expiry length of the session is 2 weeks by default)
            return redirect(self.get_success_url())

        return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        if TESTING:
            data = TEST_DATA_DEM
        else:
            data = form.cleaned_data

        participant = self.model(**data)



        # get the definition order 
        def_ids = self.set_order()
        participant.order = ','.join([str(d_id) for d_id in def_ids])

        participant.save()

        # save the participant id
        self.request.session['participantID'] = participant.id

        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):

        # get the next definition to go to
        def_count = self.request.session.get('defCount')
        def_ids = self.request.session.get('defIDs')
        next_def_id = def_ids[def_count - 1]

        print(def_count, def_ids)

        # return reverse('definitions-form', kwargs={'pk':next_def_id})
        return reverse('definition-instructions')

'''
Definition Fluency Response
'''
######################################################################

# This is a general view to handle post and get for definitions 
# For now just setting up fluency, but all that would need to change is swapping the form and changing the template a bits
# from: https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#using-formmixin-with-detailview
class DefinitionResponseView(View):

    template_name = 'definitions/definition.html'
    form_class = None
    object_model = Definition
    response_model = None


    # helper function for deciding on response type

    def set_response_type(self, request):
        # check which response type we are doing
        response_type = request.session.get('response_type')

        if response_type == 'FLUENCY':
            self.response_model = FluencyResponse
            self.form_class = FluencyResponseForm
        elif response_type == 'COMPLEXITY':
            self.response_model = ComplexityResponse
            self.form_class = ComplexityResponseForm
        else:
            raise(Exception('Response type ({}) unknown'.format(response_type)))


    def get(self, request, *args, **kwargs):

        self.set_response_type(request)
        view = DefinitionResponseDetailView.as_view(template_name=self.template_name, form_class=self.form_class, model=self.object_model, response_model=self.response_model)
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        self.set_response_type(request)
        view = DefinitionResponseFormView.as_view(template_name=self.template_name, form_class=self.form_class, model=self.object_model, response_model=self.response_model)
        return view(request, *args, **kwargs)


# View for displaying an article and form
class DefinitionResponseDetailView(DetailView):

    template_name = None
    form_class = None
    model = None
    response_model = None # for deciding between fluency or complexity

    def get_object(self, queryset=None):
        # print(self.kwargs.get(self.pk_url_kwarg))
        # pk = self.kwargs.get(self.pk_url_kwarg)
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if TESTING:
            context['form'] = self.form_class(initial=TEST_DATA_RESPONSE)
            return context
        
        # See if this participant has already filled out a response to this snippet
        # If so, populate the form with the filled in data and disable all of it (readonly) 

        def_response = get_definitionresponse_participant(self.request, self.object, self.response_model)
        if def_response is None:
            context['form'] = self.form_class()
        else:
            print('We found a def response!')
            # populate the form and disable it
            form = self.form_class(instance=def_response)
            for field in form.fields:
                form.fields[field].disabled = True
                print(form.fields[field])
                # 
            context['form'] = form

        return context

    # protecting against people going back
    def get(self, request, *args, **kwargs):
        # first check if already past the article limit
        def_count = request.session.get('defCount')
        max_def_count = request.session.get('maxDefCount')
        if def_count > max_def_count:
            return redirect('landing')
        return super().get(request, *args, **kwargs)


# view for handling form posting
class DefinitionResponseFormView(SingleObjectMixin, FormView):
    template_name = None
    form_class = None
    model = None
    response_model = None

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if TESTING:
            data = TEST_DATA_RESPONSE
        else:
            data = form.cleaned_data

        self.object = self.get_object()

        data['participant_id'] = self.request.session.get('participantID')
        data['definition_id'] = self.object.id

        print(data)

        snippet_response = self.response_model(**data)
        snippet_response.save()

        # increment snippet count
        self.request.session['defCount'] += 1
       
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        print(form.errors)
        return super().form_invalid(form)

    # fully overriding post to first catch the case where the participant had already completed this
    def post(self, request, *args, **kwargs):
        form = self.get_form()

        print('DEF_COUNT:{}'.format(self.request.session['defCount']))

        # See if this participant has already filled out a response to this snippet
        # If so just immediately skip to the next phase
        def_response = get_definitionresponse_participant(self.request, self.get_object(), self.response_model) 

        if def_response is not None:
            return redirect(self.get_success_url())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



    def get_success_url(self):

        # checks if the user has done three articles, if so sends them to the thank you page
        def_count = self.request.session.get('defCount')
        max_def_count = self.request.session.get('maxDefCount')
        if def_count > max_def_count:
            return reverse('definition-comments')
        else:
            # get another snippet to show the user from the order
            def_ids = self.request.session.get('defIDs')
            
            return reverse('definition-form', kwargs={'pk': def_ids[def_count - 1]})

######################################################################
######################################################################
######################################################################




class DefinitionCommentView(FormView):

    template_name = 'definitions/comments.html'
    form_class = CommentForm
    model = Comment
    success_url = 'thank-you'


    def form_valid(self, form):

        data = form.cleaned_data

        data['participant_id'] = self.request.session.get('participantID')

        comments = self.model(**data)

        comments.save()

        return super().form_valid(form)



def thank_you(request):
    # check that they a) exist and b) completed the last question
    participant_id = request.session.get('participantID', None)
    participant = Participant.objects.get(id=participant_id)
    code = participant.HITid

    # get the response type so we know which responses to look for
    response_type = RESPONSE_TYPE_MAP[request.session.get('response_type')]
    def_responses = get_definitionresponse_participant(request, definition=None, responseType=response_type)

    if (def_responses is not None) and (participant_id is not None):
        participant = Participant.objects.get(id=participant_id)
        code = participant.HITid
    return render(request, 'definitions/thank_you.html', {'completed': True, 'code': code})
    

