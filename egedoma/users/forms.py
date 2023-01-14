from .models import User

from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['telegram_id', 'first_name', 'telegram_username']
