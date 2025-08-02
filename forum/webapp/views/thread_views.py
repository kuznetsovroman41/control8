from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count

from ..models.thread import Thread
from ..forms.thread_form import ThreadForm

class ThreadListView(ListView):
    model = Thread
    template_name = 'webapp/thread_list.html'
    context_object_name = 'threads'
    ordering = ['-created_at']

    def get_queryset(self):
        return Thread.objects.annotate(reply_count=Count('reply'))

class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'webapp/thread_form.html'
    success_url = reverse_lazy('webapp:thread_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
