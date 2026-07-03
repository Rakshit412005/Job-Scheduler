from django.urls import path
from .views import QueueListCreateView

urlpatterns = [
    path('', QueueListCreateView.as_view()),
]