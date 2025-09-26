from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Message

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_pic','college','location','budget','hobbies',
            'nationality','country','employment','daynight',
            'gender','pref_gender','room_rules','pref_schedule'
        ]
        widgets = {
            'college': forms.TextInput(attrs={'placeholder':'College'}),
            'location': forms.TextInput(attrs={'placeholder':'Location'}),
            'budget': forms.NumberInput(attrs={'placeholder':'Budget'}),
            'hobbies': forms.Textarea(attrs={'rows':2,'placeholder':'Hobbies (comma separated)'}),
            'room_rules': forms.Textarea(attrs={'rows':2,'placeholder':'Room rules (comma separated)'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':2,'placeholder':'Type a message...','style':'resize:none;'})
        }
