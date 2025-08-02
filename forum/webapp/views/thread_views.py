from django.views.generic import ListView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Count

from ..models.thread import Thread
from ..models.answer import Answer
from ..forms.answer_form import AnswerForm
from ..forms.thread_form import ThreadForm

class ThreadListView(ListView):
    model = Thread
    template_name = 'webapp/thread_list.html'
    context_object_name = 'threads'
    ordering = ['-created_at']

    def get_queryset(self):
        return Thread.objects.annotate(reply_count=Count('answers'))


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'webapp/thread_form.html'
    success_url = reverse_lazy('webapp:thread_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ThreadDetailView(LoginRequiredMixin, DetailView, FormView):
    model = Thread
    template_name = 'webapp/thread_detail.html'
    form_class = AnswerForm

    def get_success_url(self):
        return reverse('webapp:thread_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = self.object.answers.order_by('created_at')
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            answer = form.save(commit=False)
            answer.topic = self.object
            answer.author = request.user
            answer.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
