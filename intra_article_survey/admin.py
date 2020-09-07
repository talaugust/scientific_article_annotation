from django.contrib import admin
from .models import Demographics, ArticleResponse

# Register your models here.
@admin.register(Demographics)
class DemAdmin(admin.ModelAdmin):
    list_display = ('age', 'gender', 'profession', 'HITid', 'created')


@admin.register(ArticleResponse)
class ArticleResponseAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'article_id', 'created')
