from django.urls import path

from .views import *


urlpatterns = [
    path('<str:insta_username>/parse-inst-account/', CreateInstagramAPIView.as_view()),
    path('<str:page_id>/parse-vk-page/', CreateVKPersonAPIView.as_view())
]