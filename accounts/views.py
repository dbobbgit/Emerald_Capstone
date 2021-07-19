from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-editing/
