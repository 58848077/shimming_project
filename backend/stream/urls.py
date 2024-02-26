from django.urls import path
from stream.views import StreamStatus
urlpatterns = [
    path('status/', StreamStatus.as_view()),
]