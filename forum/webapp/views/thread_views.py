from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.thread import Thread
from ..forms.answer_form import AnswerForm
from ..forms.thread_form import ThreadForm
from django.db.models import Count

class ThreadListView(ListView):
    model = Thread
    template_name = 'webapp/thread_list.html'
    context_object_name = 'threads'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        return Thread.objects.annotate(reply_count=Count('answers')).order_by('-created_at')




class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'webapp/thread_form.html'
    success_url = reverse_lazy('webapp:thread_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class ThreadDetailView(LoginRequiredMixin, DetailView, FormView):
    model = Thread
    template_name = 'webapp/thread_detail.html'
    form_class = AnswerForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers_list = self.object.answers.order_by('created_at')

        paginator = Paginator(answers_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            answers = paginator.page(page)
        except PageNotAnInteger:
            answers = paginator.page(1)
        except EmptyPage:
            answers = paginator.page(paginator.num_pages)

        context['answers'] = answers
        if 'form' not in context:
            context['form'] = self.get_form()

        user = self.request.user
        context['is_moderator'] = user.groups.filter(name='Moderator').exists()

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

    def get_success_url(self):
        return reverse('webapp:thread_detail', kwargs={'pk': self.object.pk})

class ThreadEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Thread
    fields = ['title', 'content']
    template_name = 'webapp/thread_edit.html'

    def test_func(self):
        thread = self.get_object()
        return (self.request.user == thread.author or
                self.request.user.is_superuser or
                self.request.user.groups.filter(name='Moderator').exists())

    def get_success_url(self):
        return reverse_lazy('webapp:thread_detail', kwargs={'pk': self.object.pk})


class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thread
    template_name = 'webapp/thread_confirm_delete.html'
    success_url = reverse_lazy('webapp:thread_list')

    def test_func(self):
        thread = self.get_object()
        return (self.request.user == thread.author or
                self.request.user.is_superuser or
                self.request.user.groups.filter(name='Moderator').exists())