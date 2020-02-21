from django.db import models
import uuid
from django_mysql.models import JSONField, ListTextField
from django.contrib.auth.models import User, Group


# Create your models here.
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


    # {'permissions': {'read': [], 'update': [], 'delete': [], 'admin': []}, 'user': 'Joe Bloggs', 'ranges': [{'start': '/p[1]', 'startOffset': 1, 'end': '/p[1]', 'endOffset': 143}], 'quote': 'The Trump administration violated the Clean Air Act by not taking action on harmful emissions from landfills, a federal court ruled yesterday.', 'text': 'testing', 'tags': [], 'uri': 'http://this/document/only'}