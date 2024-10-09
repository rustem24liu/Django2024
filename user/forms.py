from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=True, strip=False)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(), required=True, strip=False)

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Passwords must match')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'email')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('firstname', 'lastname', 'email')
        labels = {'firstname': 'First Name', 'lastname': 'Last Name', 'email': 'Email'}

        widgets = {'username': forms.TextInput(attrs={'class': 'form-control w-50'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control w-50'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control w-50'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control w-50'}), }
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('number', 'birth_date', 'avatar')
        labels = {'number': 'Number', 'birth_date': 'Birth Date', 'avatar': 'Avatar'}

        widgets = {'number': forms.TextInput(attrs={'class': 'form-control w-50'}),
                   'birth_date': forms.DateInput(attrs={'class': 'form-control w-50', 'type':'date'}),
                   'avatar': forms.FileInput(attrs={'class': 'form-control w-50'})}

class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True, strip=False)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True, strip=False)
    old_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Old password must match')

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            return user

        class Meta:
            model = get_user_model()
            fields = ('old_password', 'password', 'password_confirm')
