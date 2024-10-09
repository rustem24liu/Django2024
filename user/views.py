from lib2to3.fixes.fix_input import context

from django.contrib.auth import authenticate, login, logout, get_user, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from .forms import RegistrationForm, ProfileEditForm, PasswordChangeForm, UserEditForm
from .models import Profile


# Create your views here.


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('index')
        else:
            context['error'] = True
    return render(request, 'main-page/user/login.html')

@login_required
def logout_view(request):
    logout(request)
    next = request.GET.get('next')
    if next:
        return redirect(next)
    return redirect('index')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'main-page/user/register.html', context={'form': form})

class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'main-page/user/profile.html'
    context_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_object(self):
        return self.request.user

class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    form_class = UserEditForm
    template_name = 'main-page/user/profile-edit.html'
    context_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
            print(kwargs)
        return super().get_context_data(**kwargs)

    def get_profile_form(self):
        profile_form = {'instance': self.object.profile}
        if self.request.method == 'POST':
            profile_form['data'] = self.request.POST
            profile_form['files'] = self.request.FILES
            # print(profile_form)
        return ProfileEditForm(**profile_form)

    def get_success_url(self):
        return reverse('profile')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)


    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return render(context)

    def get_object(self, queryset=None):
        return self.request.user

class PasswordChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = PasswordChangeForm
    template_name = 'main-page/user/change-password.html'
    context_object_name = 'user_object'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('login')

