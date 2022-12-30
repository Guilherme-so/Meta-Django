from django.urls import path
from . import views

urlpatterns = [
    path('rating/',views.RatingsView.as_view())
]