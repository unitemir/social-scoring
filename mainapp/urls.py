from django.urls import path

from .views import *


urlpatterns = [
    path('get-stats/<str:social_network>/<str:username>/')
]
