from django.shortcuts import render
from django.core.mail import send_mail
from django.views.generic import FormView
from django.contrib.auth import authenticate, login

from accounts.forms import UserCreationForm


class RegisterView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()

        username = self.request.POST['username']
        email = self.request.POST['email']
        password = self.request.POST['password1']

        message = """
        Добро пожаловать на сайт, {}.

        Твой пароль: {}
        """.format(username, password)

        send_mail('Welcome!', message, 'HybridCraft',
                  [email], fail_silently=False)

        login(self.request, user)
        return super(RegisterView, self).form_valid(form)
