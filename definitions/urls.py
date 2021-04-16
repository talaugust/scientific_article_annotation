from django.urls import path

from . import views

urlpatterns = [
    path('landing', views.landing, name='landing'),
    path('landing/<int:response_type>', views.landing, name='landing'),
    path('demographics', views.DefinitionDemographicsView.as_view(), name='definition-demographics'),
    path('instructions', views.DefinitionInstructions, name='definition-instructions'),    
    path('form/<uuid:pk>/', views.DefinitionResponseView.as_view(), name='definition-form'),
    path('comments', views.DefinitionCommentView.as_view(), name='definition-comments'),  
    path('thank-you', views.thank_you, name='definition-thank-you'),  
]