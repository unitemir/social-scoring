from django.urls import path

from .views import *


urlpatterns = [
    path('<str:insta_username>/parse-inst/', CreateInstagramAPIView.as_view()),
    path('<str:page_id>/parse-vk/', CreateVKPersonAPIView.as_view()),
    path('<int:facebook_id>/parse-facebook/', CreateFacebookAPIView.as_view())
]