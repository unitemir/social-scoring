from django.urls import path

from .views import *


urlpatterns = [
    path('get-stats/<str:social_network>/<str:username>/', GetSocialNetworksStatsView.as_view()),
    path('persons/', show_persons)
]
