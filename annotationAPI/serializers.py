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
        fields = ['id', 'text', 'title', 'uri', 'lead', 'site']


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['id', 'text', 'quote', 'permissions', 'user', 'ranges', 'tags', 'uri', 'article']


    # def find_article(self, article_id):
    #     print("finding articles")
    #     articles = Article.objects.all()
    #     # find the article matching the url of the current article
    #     try:
    #         matched_article = articles.get(id=article_id)
    #     except:
    #         raise serializers.ValidationError("Article does not exist")
    #     return matched_article

    # def is_valid(self):
    #     article = self.find_article(self.initial_data['uri'])
    #     self.initial_data['article'] = article.id
    #     return super().is_valid()

        # tags = self.initial_data['tags']
        # if len(tags) < 1:
        #   tags = ['']

    #   # # do some changing of the data here to be a 
    #   # self.initial_data['tags'] = tags


    # def create(self, validated_data):
    #     return self.model.objects.create(**validated_data)