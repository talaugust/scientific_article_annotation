from django.contrib.auth.models import User, Group
from annotationAPI.serializers import UserSerializer, GroupSerializer, AnnotationSerializer, ArticleSerializer, AnnotationHITSerializer
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Annotation, Article, AnnotationHIT, AnnotationHITStories, AnnotationHITExplAna, AnnotationHITParagraph
from .forms import AnnotationHITForm, AnnotationHITStoriesForm, AnnotationHITExplAnaForm, AnnotationHITParagraphForm
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, Http404
from django.views import View
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import json
import uuid
import string



TESTING = False 
# TEST_DATA = {'age': 24, 'gender': 'MALE', 'gender_self_describe': '', 'english_prof': 'NATIVE', 'agree_to_contact': False, 'comments': '24', 'enjoy': 1, 'objective': 1, 'is_lead': 1, 'lead_interest': 1, 'is_main_points_highlight': True, 'is_care_highlight': True, 'is_conclusion': 1, 'is_story_highlight': True, 'is_personal_highlight': True, 'is_expl_highlight': True, 'is_analogy_highlight': True, 'user_id': 8, 'article_id': '366fbfbf-c9c0-407d-8f51-d7826930ed41'}
TEST_DATA = { 'comments': '24', 'is_lead': 1, 'lead_interest': 1, 'is_main_points_highlight': True, 'is_care_highlight': True, 'is_conclusion': 1, 'is_story_highlight': True, 'is_personal_highlight': True, 'is_expl_highlight': True, 'is_analogy_highlight': True, 'user_id': 8, 'article_id': '366fbfbf-c9c0-407d-8f51-d7826930ed41'}



def home(request):
    context = {}
    if request.user.is_superuser:
        context['super'] = True
        # get all annotated articles from all users
        users = User.objects.all()
        user_articles = {}
        for user in users:
            user_articles[user.username] = Article.objects.getUserAnnotated(user)
        context['user_articles'] = user_articles
        
    elif request.user.is_authenticated:
        context['super'] = False 
        annotated_articles = Article.objects.getUserAnnotated(request.user)
        context['articles'] = annotated_articles
        

    return render(request, 'registration/home.html', context)

#############################################################################################
########### ########### ########### LITW specific views ########### ########### ############# 
#############################################################################################
# def consent(request):
#     return render(request, 'consent.html')

# def instructions(request):
#     return render(request, 'instructions.html')

# def results(request):
#     return render(request, 'results.html')

#############################################################################################
########### ########### ########### Turk specific views ########### ########### ############# 
#############################################################################################

# super simple view function for displaying the hitcode
def HITcode(request, code):
    if request.user.is_authenticated:
        return render(request, 'HITcode.html', {'completed': True, 'code': code})
    else: 
        return render(request, 'HITcode.html', {'completed': False, 'code': None})



#############################################################################################
########### ###########  Article views (not part of the API) ########### ########### ########
#############################################################################################

# This is a general view to handle post and get for articles 
# from: https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#using-formmixin-with-detailview
class ArticleView(LoginRequiredMixin, View):

    HITclass = None
    login_url = '/accounts/login/'

    def set_classes(self):
        HITclass = self.kwargs.get('HITclass', None)
        if HITclass == 'paragraph':
            self.form_class = AnnotationHITParagraphForm
            self.model_class = AnnotationHITParagraph
        elif HITclass == 'expl':
            self.form_class = AnnotationHITExplAnaForm
            self.model_class = AnnotationHITExplAna
        elif HITclass == 'story':
            self.form_class = AnnotationHITStoriesForm
            self.model_class = AnnotationHITStories
        elif HITclass == 'all':
            self.form_class = AnnotationHITForm
            self.model_class = AnnotationHIT
        # default
        else:
            self.form_class = AnnotationHITForm
            self.model_class = AnnotationHIT
        

    def get(self, request, *args, **kwargs):
        self.set_classes()
        view = ArticleDetailView.as_view(form_class=self.form_class)
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_classes()
        view = ArticleHITFormView.as_view(form_class=self.form_class, HITmodel=self.model_class)
        return view(request, *args, **kwargs)


######### GET ##########
class ArticleDetailView(LoginRequiredMixin, DetailView):
    template_name = 'article_base.html'
    model = Article
    form_class = None
    login_url = '/accounts/login/'

    def set_form_class(self, form_class):
        self.form_class = form_class

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if TESTING:
            context['form'] = self.form_class(initial=TEST_DATA)
        else: 
            context['form'] = self.form_class()
        context['HITtype'] = context['form'].label
        return context

    # adding a section to log in a user automatically here
    def get(self, request, *args, **kwargs):

        # # there is no user in this session`
        # if not request.user.is_authenticated:

        #     # make a new user with a random name and password
        #     username = uuid.uuid4()
        #     password = uuid.uuid4()
        #     user = User.objects.create_user(username=username, password=password)
        #     # set password to unusable, since we won't be having participants log in anywhere
        #     # user.set_unusable_password()
        #     user.save()

        #     # authenticate the user
        #     user = authenticate(username=username, password=password)

        #     # log the user in
        #     login(request, user)

        return super().get(request, *args, **kwargs)

######### POST ##########
class ArticleHITFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'article_base.html'
    form_class = None
    model = Article
    HITmodel = None
    login_url = '/accounts/login/'

    def set_form_class(self, form_class):
        self.form_class = form_class

    def form_valid(self, form):
        """If the form is valid, add in article and user, save and redirect to the supplied URL."""
        if TESTING:
            data = TEST_DATA
        else:
            data = form.cleaned_data
        data['user_id']= self.request.user.id
        data['article_id'] = self.object.id
        if data['lead_interest'] == '':
            data['lead_interest'] = 0
        # print(data)

        HIT = self.HITmodel(**data)
        HIT.save()
        # form.save()
        # save user_id
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        print(form.errors)
        return super().form_invalid(form)
        

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        # form = self.get_form()
        # print(form.data)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('random-article-detail', kwargs={'HIT': 'None', 'HITclass': 'all'})
        # return reverse('HIT-code', kwargs={'code': code})



def rand_article(request):
    return redirect(reverse('random-article-detail', kwargs={'HIT': 'None', 'HITclass': 'all'}))

# wrapper view function for getting a random article if you just go to articles/ url
# HIT is 0 for if this is not as AMT HIT, 1 if it is. 
# right now that changes what articles can be viewed
def randomArticle(request, HIT, HITclass='all'):
    print(HIT, HITclass)
    # get a random pk for an article 
    if HIT == 'HIT':
        # filter based on if it is HITable, and if it has two annotation HITs on it
        queryset = Article.objects.isHITAvaliable()
    else:
        queryset = Article.objects.all()

    random_article = queryset.order_by('?').first()

    try:
        return redirect('article-detail', pk=random_article.id, HITclass=HITclass)
    except AttributeError: 
        raise Http404("No articles exist")


#############################################################################################
########### ########### ###########  API endpoints ########### ########### ######## #########
#############################################################################################

"""
    API endpoints
"""
@api_view(['GET'])
def root(request):  
    """
    returns: object containing store metadata, including API version
    """
    if request.method == 'GET':
        response = {'name': 'Annotator Store API', 'version': '1.2.10 (annotator.js)'}
        return Response(response)

@api_view(['GET', 'POST'])
def annotations(request):
    """
    returns: object containing store metadata, including API version
    """
    if request.method == 'GET':
        response = {'name': 'Annotator Store API', 'version': '1.2.10 (annotator.js)'}
        return Response(response)

    if request.method == 'POST':
        response = {'name': 'Annotator Store API', 'version': '1.2.10 (annotator.js)'}
        print(request.data)
        return Response(response)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer



class AnnotationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows annotations
    """
    permission_classes = [IsAuthenticated]
    queryset = Annotation.objects.all()
    # model = Annotation
    serializer_class = AnnotationSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        if self.request.user.is_superuser:
             # return all the annotations
             annotations = self.queryset
        else:
            annotations = self.queryset.filter(user=self.request.user.id)
        return annotations

    def create(self, request):
        # copy data and override user
        data = request.data
        data['user'] = request.user.id 
        print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        print(serializer.errors)
        serializer.save()  
        return Response(serializer.data)


    def list(self, request): 
        article_id = request.GET.get('id', None)
        limit = request.GET.get('limit', len(self.get_queryset()))

        if article_id is None:
            # return all the annotations
            filtered_queryset = self.get_queryset()[:int(limit)]   
        else:
            filtered_queryset = self.get_queryset().filter(article=article_id)[:int(limit)]  

        serializer = self.serializer_class(filtered_queryset, many=True)
        annotations = {'rows': serializer.data, 'total':len(serializer.data)}   
        return Response(annotations)


class AnnotationHITViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AnnotationHIT.objects.all()
    serializer_class = AnnotationHITSerializer
    
    permission_classes = (IsAdminUser,)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    permission_classes = (IsAdminUser,)



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    permission_classes = (IsAuthenticated,)




