from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout, login
from django.views.generic import FormView

# from djangotravelmap.users_app.forms import LoginUserForm
from . import forms


class RegisterFormView(FormView):
    form_class = forms.RegisterUserForm # Форма для регистрации
    success_url = '/' # Успешная регистрация
    template_name = 'users_app/registration.html' # Шаблон с формой

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Авторизация")
    #     return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)

class LoginFormView(FormView):
    form_class = forms.LoginUserForm # Форма для авторизации
    success_url = '/' # Успешная регистрация
    template_name = 'users_app/authorization.html' # Шаблон с формой

    def form_valid(self, form):

        return super(LoginFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(LoginFormView, self).form_invalid(form)

def logout_user(request):
    logout(request)
    return redirect('/')

# def registration(request):
#     # u = reverse('./admin')
#     # return HttpResponse('a')
#
#     # return HttpResponseRedirect('admin')
#     # return HttpResponseRedirect(url_redirect)
#     # return redirect(url_redirect)
#     return render(request, 'users_app/registration.html')
#
# def authorization(request):
#     # url_redirect = reverse('admin')
#     # return HttpResponseRedirect(url_redirect)
#
#     # return redirect(url_redirect)
#     return render(request, 'users_app/authorization.html')

