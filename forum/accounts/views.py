from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms.user import CustomUserCreationForm
from django.views.generic import DetailView
from django.db.models import Count
from webapp.models.thread import Thread
from webapp.models.answer import Answer
User = get_user_model()

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context['answer_count'] = Answer.objects.filter(author=user).count()
        context['user_threads'] = Thread.objects.filter(author=user).annotate(reply_count=Count('answers')).order_by('-created_at')
        return context
