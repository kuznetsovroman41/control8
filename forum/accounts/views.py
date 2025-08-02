from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms.user import CustomUserCreationForm

User = get_user_model()

class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('accounts:login')
