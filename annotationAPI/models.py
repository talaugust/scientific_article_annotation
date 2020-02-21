from django.db import models
import uuid
from django_mysql.models import JSONField, ListTextField
from django.contrib.auth.models import User, Group


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    title = models.TextField()
    uri = models.URLField()
    lead = models.TextField(blank=True)
    site = models.TextField()

class Annotation(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)
    quote = models.TextField(blank=False)
    permissions = JSONField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    ranges = JSONField()
    tags = JSONField(blank=True)
    uri = models.URLField()
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )





