from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Annotation, Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'text', 'title', 'uri', 'lead', 'site', 'HITable']


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['id', 'text', 'quote', 'permissions', 'user', 'ranges', 'tags', 'uri', 'article']
