from django.contrib import admin
from .models import Annotation, Article, AnnotationHIT

# Register your models here.
admin.site.register(Annotation)
admin.site.register(Article)
admin.site.register(AnnotationHIT)
