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
        fields = ['id', 'text', 'quote', 'permissions', 'user', 'ranges', 'tags', 'uri', 'article_id']


    def find_article(self):
    	articles = Article.objects.all()
    	# find the article matching the url of the current article
    	matched_article = articles.get(uri=self.initial_data['uri'])
    	print(matched_article)
    	return matched_article.id

    def is_valid(self):
    	print(self.initial_data['tags'])
    	article_id = self.find_article()
    	self.initial_data['article_id'] = article_id 
    	print(article_id)
    	return super().is_valid()

    	# tags = self.initial_data['tags']
    	# if len(tags) < 1:
    	# 	tags = ['']

    # 	# # do some changing of the data here to be a 
    # 	# self.initial_data['tags'] = tags


    # def create(self, validated_data):
    #     return self.model.objects.create(**validated_data)