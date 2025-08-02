from django.urls import path
from .views.thread_views import ThreadListView, ThreadCreateView, ThreadDetailView
from .views.answer_views import AnswerEditView, AnswerDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', ThreadListView.as_view(), name='thread_list'),
    path('create/', ThreadCreateView.as_view(), name='thread_create'),
    path('threads/<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('answers/<int:pk>/edit/', AnswerEditView.as_view(), name='answer_edit'),
    path('answers/<int:pk>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
]








