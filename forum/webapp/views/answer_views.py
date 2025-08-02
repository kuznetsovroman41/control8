from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from ..models.answer import Answer
from ..forms.answer_form import AnswerForm

class AnswerEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'webapp/answer_form.html'

    def get_success_url(self):
        return reverse_lazy('webapp:thread_detail', kwargs={'pk': self.object.topic.pk})

    def test_func(self):
        user = self.request.user
        answer = self.get_object()
        return (
                user.is_superuser or
                user.groups.filter(name='Moderator').exists() or
                answer.author == user
        )


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'webapp/answer_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('webapp:thread_detail', kwargs={'pk': self.object.topic.pk})

    def test_func(self):
        user = self.request.user
        answer = self.get_object()
        return (
                user.is_superuser or
                user.groups.filter(name='Moderator').exists() or
                answer.author == user
        )

