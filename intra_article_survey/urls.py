from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('instructions/', views.instructions, name='instructions'),
    path('demographics/', views.DemographicsView.as_view(), name='demographics'),
    path('article/<uuid:pk>/', views.ArticleResponseView.as_view(), name='article-response-form'),
    path('thank_you/', views.thank_you, name='thank_you'),
]