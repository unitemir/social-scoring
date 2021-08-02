from django.urls import path

from .views import *


urlpatterns = [
    path('<str:insta_username>/parse-inst-account/', CreateInstagramAPIView.as_view()),
]