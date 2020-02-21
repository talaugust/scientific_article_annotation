from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Annotation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ['id', 'text', 'quote', 'permissions', 'user', 'ranges', 'tags', 'uri']

    # def is_valid(self):
    # 	print(self.initial_data['tags'])
    # 	# tags = self.initial_data['tags']
    # 	# if len(tags) < 1:
    # 	# 	tags = ['']

    # 	# # do some changing of the data here to be a 
    # 	# self.initial_data['tags'] = tags

    # 	return super().is_valid()

    # def create(self, validated_data):
    #     return self.model.objects.create(**validated_data)