from django.contrib.auth.models import User, Group
from annotationAPI.serializers import UserSerializer, GroupSerializer, AnnotationSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import Annotation
import json




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


class AnnotationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows annotations
    """
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer

    def create(self, request):
        # print(request.data)
        # print(request.data['quote'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        # print(serializer.errors)
        # print(serializer)  
        serializer.save()  
        return Response(serializer.data)


    def list(self, request): 
        # print(request.GET['uri'])  
        # print(request.GET['uri']) 
        uri = request.GET.get('uri', "http://docs.annotatorjs.org/en/v1.2.x/")
        limit = request.GET.get('limit', len(self.queryset))
        print(limit)
        print(uri) 
        filtered_queryset = self.queryset.filter(uri=uri)[:int(limit)]   


        serializer = self.serializer_class(filtered_queryset, many=True)
        print(serializer.data)

        annotations = {'rows': serializer.data, 'total':len(serializer.data)}

        return Response(annotations)

    @action(detail=False, methods=['GET'])
    def search(self, request):
        print(self.kwargs.get('uri'))
        annotations = self.queryset.get(uri=uri)

        # print(annotations)
        serializer = self.get_serializer(annotations, many=True)
        return Response(serializer.data)


    # def list(self, request):
    #     return Response(self.queryset)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

