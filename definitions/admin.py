from django.contrib import admin
from .models import Participant, Definition, Term, FluencyResponse, ComplexityResponse, Comment

# Register your models here.
@admin.register(Definition)
class DefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'term_id', 'model', 'def_text')

# Register your models here.
@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('id', 'term_text', 'category')

# Register your models here.
@admin.register(FluencyResponse)
class FluencyResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'definition', 'fluency_rating', 'relevancy_rating', 'created')

# Register your models here.
@admin.register(ComplexityResponse)
class ComplexityResponse(admin.ModelAdmin):
    list_display = ('id', 'definition', 'complexity_rating', 'understand_rating', 'created')


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant', 'comment_text')

# Register your models here.
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'english_prof', 'education', 'stem_exp', 'HITid', 'created')