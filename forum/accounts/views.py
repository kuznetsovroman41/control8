from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms.user import CustomUserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('accounts:login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

