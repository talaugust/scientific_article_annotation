from django.urls import include, path
from rest_framework import routers
from annotationAPI import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

APIrouter = routers.DefaultRouter()
APIrouter.register(r'annotations', views.AnnotationViewSet)
APIrouter.register(r'articles', views.ArticleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(APIrouter.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-test/', views.root),
    path('api-test/annotations', views.annotations)
]