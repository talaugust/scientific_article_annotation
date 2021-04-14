from django.urls import include, path
from rest_framework import routers
from annotationAPI import views as annotationViews

from django.contrib import admin
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'users', annotationViews.UserViewSet)
router.register(r'groups', annotationViews.GroupViewSet)

APIrouter = routers.DefaultRouter()
APIrouter.register(r'annotations', annotationViews.AnnotationViewSet)

# note that this router is api/articles while the class view below is just articles/ because it is not really part of the API
APIrouter.register(r'articles', annotationViews.ArticleViewSet)

APIrouter.register(r'hits', annotationViews.AnnotationHITViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', annotationViews.home, name='home'),
    path('home/<str:order>', annotationViews.home, name='home'),  
    path('', include(router.urls)),
    path('api/', include(APIrouter.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-test/annotations', annotationViews.annotations),
    path('articles/<uuid:pk>/', annotationViews.ArticleView.as_view(HITclass='all'), name='article-detail'), # depreciated
    path('articles/<str:HITclass>/<uuid:pk>/', annotationViews.ArticleView.as_view(), name='article-detail'),
    path('articles/<str:HIT>/', annotationViews.randomArticle, name='random-article-detail'),
    path('articles/<str:HIT>/<str:HITclass>/', annotationViews.randomArticle, name='random-article-detail'),
    path('HIT/<str:code>/', annotationViews.HITcode, name='HIT-code'), 
    path('article/', annotationViews.rand_article, name='rand-article'), 
    # path('LITW/consent', annotationViews.consent, name='LITW-consent'), 
    # path('LITW/instructions', annotationViews.instructions, name='LITW-instructions'), 
    # path('LITW/results', annotationViews.results, name='LITW-results'),
    path('survey/', include('intra_article_survey.urls')),
    path('definitions/', include('definitions.urls')),
    path('tool/', include('reader_tool.urls')),
]

