from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)
from app_galpal.views import *
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'interests', InterestsViewSet)
router.register(r'profilequestions', MatchProfileQuestionsViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('profile/', get_profile),
    path('create_user/', create_user),
    path('refresh/', TokenRefreshView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
]

if settings.DEBUG:
   from django.conf.urls.static import static
   # we're adding something to the url pattern to handle the images when we're in local development
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
