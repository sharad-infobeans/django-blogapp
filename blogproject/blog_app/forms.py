from django import forms
from django.contrib.auth.models import User
from blog_app.models import UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password'].widget.attrs.update({'class':'form-control'})

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('social_handle','profile_pic')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['social_handle'].widget.attrs.update({'placeholder': 'Social Handles', 'class': 'form-control'})
        self.fields['profile_pic'].widget.attrs.update({'placeholder': 'Profile Picture', 'class': 'form-control'})