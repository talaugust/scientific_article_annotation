from django.contrib import admin
from .models import Participant, Definition, Term, FluencyResponse, ComplexityResponse, Comment
from django.core import serializers
from django.http import HttpResponse
import csv



def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


# Register your models here.
@admin.register(Definition)
class DefinitionAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'term_id', 'model', 'def_text')
    actions = ['export_as_csv']

# Register your models here.
@admin.register(Term)
class TermAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'term_text', 'category')
    actions = ['export_as_csv']

# Register your models here.
@admin.register(FluencyResponse)
class FluencyResponseAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'definition', 'fluency_rating', 'relevancy_rating', 'created')
    actions = ['export_as_csv']

# Register your models here.
@admin.register(ComplexityResponse)
class ComplexityResponse(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'definition', 'complexity_rating', 'understand_rating', 'created')
    actions = ['export_as_csv']


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'participant', 'comment_text')
    actions = ['export_as_csv']

# Register your models here.
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('id', 'english_prof', 'education', 'stem_exp', 'HITid', 'created')
    actions = ['export_as_csv']