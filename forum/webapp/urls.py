from django.urls import path
from .views.thread_views import ThreadListView, ThreadCreateView

app_name = 'webapp'

urlpatterns = [
    path('', ThreadListView.as_view(), name='thread_list'),
    path('create/', ThreadCreateView.as_view(), name='thread_create'),
]







