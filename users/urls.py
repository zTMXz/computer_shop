from django.urls import path, include
from users.views import Register, profile, send_mail_to_Egor

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("register/", Register.as_view(), name='register'),
    path("profile/", profile, name='profile'),
    path("egor/", send_mail_to_Egor, name='egor'),

]