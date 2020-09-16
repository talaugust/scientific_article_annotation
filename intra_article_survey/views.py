from django.shortcuts import render, redirect, reverse
from annotationAPI.models import Annotation, Article
from django.views.generic.edit import FormView
from .models import Demographics, ArticleResponse, GeneralEndQuestions
from .forms import DemographicsForm, ArticleResponseForm, GeneralEndQuestionsForm
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views import View
import uuid
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from article_annotation.settings import DEBUG


TESTING = DEBUG  
TEST_DATA_DEM = {'age': 12, 'gender': 'FEMALE', 'gender_self_describe': '', 'english_prof': 'LIMIT', 'education': 'HIGH', 'stem_background': '1-3', 'sci_info_time': 'DAILY', 'sci_info': ['Magazines', 'LIBRARY'], 'profession': 'Tal', 'user_id': 6, 'research_involved':'1'}
TEST_DATA_RESPONSE = {'enjoy': 1, 'is_most_interesting_highlight': True, 'is_difficult_highlight': False, 'int_why': 'TEST', 'user_id': 6, 'article_id': '2b76323f-40f7-47eb-8f33-655da6541e15'}
TEST_END_RESPONSE = {'sci_info_time_open': 'DAILY', 'open_comments': 'TEST', 'user_id': 57}
ARTICLE_COUNT = 2


# IDS for articles used in our survey, selected as a randmized, stratified sample from the full dataset
SURVEY_ARTICLE_IDS = ['1449d9ad-0fbb-47af-8925-bbdf5a99e265', 
 '24572868-498b-4734-a508-44302ec94ad0', 
 'cec343fd-1252-4456-b233-a5ed6ff39be6',
 '32d1eca1-389a-4583-bd10-833c62ce9816',
 '10ab437c-0f75-4ca4-adee-7bb813aaaecb',
 'f37f8677-ca82-4d50-ad32-e5e378488d25',
 'fb812013-c0e9-4cb8-aace-6a5e44c657f1',
 '1e91c25e-d709-4e03-a983-69caa949a1b0',
 ]



#  # helper function for getting the articles for the study
# def get_articles(request):
#     articles = Article.objects.getNotUserAnnotated(user=request.user).filter(id__in=SURVEY_ARTICLE_IDS).order_by('?')
#     article_ids = [articles.first().id, articles.last().id]
#     print(article_ids)
#     return article_ids


def landing(request):
    return render(request, 'consent.html', {})


def instructions(request):
    # get a new article to go to after the instructions 
    # article_count = self.request.session.get('article_count')
    # article_ids = self.request.session.get('article_ids')
    # new_article_id = article_ids[article_count - 1]

    # return render(request, 'instructions.html', {'pk': new_article_id})
    new_article = Article.objects.getNotUserAnnotated(user=request.user).filter(id__in=SURVEY_ARTICLE_IDS).order_by('?').first()
    return render(request, 'instructions.html', {'pk': new_article.id})

def thank_you(request):

    # try to get the hitcode based on if this person is logged in and completed the demographics
    user = request.user 
    # print('User: {}'.format(user))
    try:
        user_dem = Demographics.objects.filter(user_id=user.id).order_by('-id')[0]
        # and they completed three articles
        # print('ARTICLE COUNT: {}'.format(request.session.get('article_count')))
        if request.session.get('article_count') > ARTICLE_COUNT:
            return render(request, 'thank_you.html', {'code': user_dem.HITid})
        else:
            return render(request, 'thank_you.html', {})
    except:
        return render(request, 'thank_you.html', {})


# def dem(request):
#     return render(request, 'demographics.html', {})



class EndQuestionsView(FormView):
    template_name = 'end_questions.html'
    form_class = GeneralEndQuestionsForm
    model = GeneralEndQuestions

    def get_success_url(self):
        return reverse('thank_you')


    # overriding to add in testing infrastructure
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if TESTING:
            context['form'] = self.form_class(initial=TEST_END_RESPONSE)
        else: 
            context['form'] = self.form_class()
        return context

    def form_valid(self, form):

        if TESTING:
            data = TEST_END_RESPONSE
        else:
            data = form.cleaned_data


        data['user_id']= self.request.user.id
        print(data)
        end_questions = self.model(**data)
        end_questions.save()
        return super().form_valid(form)

class DemographicsView(FormView):

    template_name = 'demographics.html'
    form_class = DemographicsForm
    model = Demographics
    article_model = Article



    # helper function for making a new user (with a random password) and logging them in
    # this is how we are getting around django's auth system, and make it work for us a bit
    # also this sets the user's session article count to 1 (starting at one, going to > 3)
    def make_user(self):

        # if there is already a user, make a new one
        if self.request.user.is_authenticated:
            logout(self.request)

        self.request.session['article_count'] = 1

        # make a new user with a random name and password
        username = uuid.uuid4()
        password = uuid.uuid4()
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # authenticate the user
        user = authenticate(username=username, password=password)

        # log the user in
        login(self.request, user)

        return user

        
    # overriding to add in testing infrastructure
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if TESTING:
            context['form'] = self.form_class(initial=TEST_DATA_DEM)
        else: 
            context['form'] = self.form_class()
        return context

    # adding a section to log in a user automatically here before they fill out the form
    def get(self, request, *args, **kwargs):
        user = self.make_user()
        # article_ids = get_articles(self.request)

        # self.request.session['article_ids'] = article_ids
        
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        print('Form valid')

        if TESTING:
            data = TEST_DATA_DEM
        else:
            data = form.cleaned_data

        data['user_id']= self.request.user.id
        print(data)
        dems = self.model(**data)
        dems.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('instructions')
        # new_article = self.article_model.objects.getNotUserAnnotated(user=self.request.user).filter(id__in=SURVEY_ARTICLE_IDS).order_by('?').first()
        # return reverse('article-response-form', kwargs={'pk': new_article.id})




# This is a general view to handle post and get for articles 
# from: https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#using-formmixin-with-detailview
class ArticleResponseView(View):

    template_name = 'article_form.html'
    form_class = ArticleResponseForm
    object_model = Article
    response_model = ArticleResponse


    def get(self, request, *args, **kwargs):
        view = ArticleResponseDetailView.as_view(template_name=self.template_name, form_class=self.form_class, model=self.object_model)
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArticleResponseFormView.as_view(template_name=self.template_name, form_class=self.form_class, model=self.object_model, response_model=self.response_model)
        return view(request, *args, **kwargs)


# View for displaying an article and form
class ArticleResponseDetailView(DetailView):

    template_name = None
    form_class = None
    model = None

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if TESTING:
            context['form'] = self.form_class(initial=TEST_DATA_RESPONSE)
        else: 
            context['form'] = self.form_class()

        context['max_count'] = ARTICLE_COUNT

        return context

    def get(self, request, *args, **kwargs):
        # first check if already past the article limit
        article_count = request.session.get('article_count')
        if article_count > ARTICLE_COUNT:
            return redirect('end_question')
        return super().get(request, *args, **kwargs)

# view for handling form posting
class ArticleResponseFormView(SingleObjectMixin, FormView):
    template_name = None
    form_class = None
    model = None
    response_model = None


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        if TESTING:
            data = TEST_DATA_RESPONSE
        else:
            data = form.cleaned_data
        data['user_id']= self.request.user.id
        data['article_id'] = self.object.id

        print(data)

        article_response = self.response_model(**data)
        article_response.save()

        # increment completed articles
        self.request.session['article_count'] += 1
       
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        print(form.errors)
        return super().form_invalid(form)


    def get_success_url(self):

        # checks if the user has done three articles, if so sends them to the thank you page
        article_count = self.request.session.get('article_count')
        if article_count > ARTICLE_COUNT:
            return reverse('end_question')
        else:
            # get another article to show the user
            new_article = self.model.objects.getNotUserAnnotated(user=self.request.user).filter(id__in=SURVEY_ARTICLE_IDS).order_by('?').first()
            return reverse('article-response-form', kwargs={'pk': new_article.id})
