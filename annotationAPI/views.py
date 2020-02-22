from django.contrib.auth.models import User, Group
from annotationAPI.serializers import UserSerializer, GroupSerializer, AnnotationSerializer, ArticleSerializer
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import Annotation, Article
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import json
import uuid

"""
    Article views (not part of the API)
"""
class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return super().get_object(queryset)

    # adding a section to log in a user automatically here
    def get(self, request, *args, **kwargs):
        # # there is no user in this session
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
        #     print('LOGINED')

        # print(request.user)

        return super().get(request, *args, **kwargs)


# wrapper view function for getting a random article if you just go to articles/ url
def randomArticle(request):
    # get a random pk for an article 
    random_article = Article.objects.order_by('?').first()
    return redirect('article-detail', pk=random_article.id)
    # (ArticleDetailView.as_view(template_name='article_base.html')(request, pk=random_article.id))


"""
    API endpoints
"""
@api_view(['GET'])
def root(request):
    """
    returns: object containing store metadata, including API version
    """
    if request.method == 'GET':
        response = {'name': 'Annotator Store Dummy API', 'version': '1.2.10 (annotator.js)'}
        return Response(response)

@api_view(['GET', 'POST'])
def annotations(request):
    """
    returns: object containing store metadata, including API version
    """
    if request.method == 'GET':
        response = {'name': 'Annotator Store Dummy API', 'version': '1.2.10 (annotator.js)'}
        return Response(response)

    if request.method == 'POST':
        response = {'name': 'Annotator Store Dummy API', 'version': '1.2.10 (annotator.js)'}
        print(request.data)
        return Response(response)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


    # permission_classes = (IsAuthenticated,)
 
    # def create(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid()
    #     print(serializer.errors)
    #     serializer.save()  
    #     return super().create(request)


class AnnotationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows annotations
    """
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    # permission_classes = (IsAuthenticated,)



    def create(self, request):

        print('Here')
        print(request.user)

        # request.data['user'] = 1
        # request.data['user'] = request.user.id # ovverride passed user (eventually won't be passed in .data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        print(serializer.errors)
        serializer.save()  
        return Response(serializer.data)


    def list(self, request): 
        article_id = request.GET.get('id', None)
        limit = request.GET.get('limit', len(self.queryset))
        filtered_queryset = self.queryset.filter(article=article_id)[:int(limit)]   
        serializer = self.serializer_class(filtered_queryset, many=True)
        annotations = {'rows': serializer.data, 'total':len(serializer.data)}
        return Response(annotations)

    # @action(detail=False, methods=['GET'])
    # def search(self, request):
    #     print(self.kwargs.get('uri'))
    #     annotations = self.queryset.get(uri=uri)

    #     # print(annotations)
    #     serializer = self.get_serializer(annotations, many=True)
    #     return Response(serializer.data)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    permission_classes = (IsAuthenticated,)



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    permission_classes = (IsAuthenticated,)



# class CustomAuthToken(ObtainAuthToken):

#     def get(self, request, *args, **kwargs):
#         # serializer = self.serializer_class(data=request.data,
#         #                                    context={'request': request})
#         # serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']

#         token, created = Token.objects.get_or_create(user=request.user)
#         return Response({
#             'token': token.key,
#         })


