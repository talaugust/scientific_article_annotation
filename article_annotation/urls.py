from django.urls import include, path
from rest_framework import routers
from annotationAPI import views
from django.contrib import admin
from django.contrib.auth import views as auth_views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

APIrouter = routers.DefaultRouter()
APIrouter.register(r'annotations', views.AnnotationViewSet)

# note that this router is api/articles while the class view below is just articles/ because it is not really part of the API
APIrouter.register(r'articles', views.ArticleViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', views.home, name='home'), 
    path('', include(router.urls)),
    path('api/', include(APIrouter.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-test/annotations', views.annotations),
    path('articles/<uuid:pk>/', views.ArticleView.as_view(HITclass='all'), name='article-detail'), # depreciated
    path('articles/<str:HITclass>/<uuid:pk>/', views.ArticleView.as_view(), name='article-detail'),
    path('articles/<str:HIT>/', views.randomArticle, name='random-article-detail'),
    path('articles/<str:HIT>/<str:HITclass>/', views.randomArticle, name='random-article-detail'),
    path('HIT/<str:code>/', views.HITcode, name='HIT-code'), 
    path('article/', views.rand_article, name='rand-article'), 
    # path('LITW/consent', views.consent, name='LITW-consent'), 
    # path('LITW/instructions', views.instructions, name='LITW-instructions'), 
    # path('LITW/results', views.results, name='LITW-results'),
]

