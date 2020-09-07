from django.contrib import admin
from .models import Annotation, Article, AnnotationHIT


# Register your models here.
@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'article_id', 'text', 'quote', 'created')



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'uri', 'site')


@admin.register(AnnotationHIT)
class AnnotationHITAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'article_id', 'comments', 'created')

