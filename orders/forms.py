from django import forms
from .models import Order
from users.models import User


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

        user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())