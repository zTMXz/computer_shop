from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = {"username", "email"}


class UserUpdateForm(UserChangeForm):
    password = None
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', ]
        exclude = ('publisher',)
