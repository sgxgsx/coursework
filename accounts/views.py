from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from .forms import MyUserCreationForm
from dashboard.utils import populate_db


class SignUp(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'







