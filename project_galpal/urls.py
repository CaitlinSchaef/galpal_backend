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
    path('create-user/', create_user),
    path('get-questions/', get_profile_questions),
    path('get-answers/', get_profile_answers),
    path('get-all-answers/', get_all_profile_answers),
    path('update-answer/<int:pk>/', update_answer),
    path('create-answer/', create_answer),
    path('create-interest-inventory/', create_interest_inventory),
    path('get-interest-inventory/', get_interest_inventory),
    path('get-all-interest-inventories/', get_all_interest_inventories),
    path('update-interest-inventory/', update_interest_inventory),
    path('get-interests/', get_interests),
    path('create-match-profile/', create_match_profile),
    path('get-match-profile/', get_match_profile), 
    path('get-all-match-profiles/', get_all_match_profiles), 
    path('update-match-profile/', update_match_profile), 
    path('create-match-request/', create_match_request),
    path('get-match-requests/', get_match_requests),
    path('update-match-request/<int:id>/', update_match_request),
    path('create-message-channel/', create_message_channel),
    path('get-message-channel/', get_message_channel),
    path('create-message/', create_message),
    path('get-messages/', get_messages),
    path('get-friends-list/', get_friends_list),
    path('delete-user/', delete_user),
    path('refresh/', TokenRefreshView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
]

if settings.DEBUG:
   from django.conf.urls.static import static
   # we're adding something to the url pattern to handle the images when we're in local development
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
