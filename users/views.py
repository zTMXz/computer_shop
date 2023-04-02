from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserCreationForm, UserUpdateForm


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)


        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=password)

            login(request, user)

            # #РАБОТАЕТ, ПОТОМ ПЕРЕПИСАТЬ
            # send_mail(subject='Successful Registration Message',
            #           message= f"""
            #             You have successfully registered on EV_Chargers
            #             Your login details:
            #             ===============================
            #                 username: {username}
            #                 password: {password}
            #             ===============================
            #           """,
            #           recipient_list=[email],
            #           from_email=DEFAULT_FROM_EMAIL
            #           )

            return redirect('home')



        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect("login")

    form = UserUpdateForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('profile')

    context = {
        "form": form,
    }

    return render(request, template_name="registration/profile.html", context=context)
