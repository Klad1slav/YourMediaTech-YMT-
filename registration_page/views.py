from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optional: Log the user in after register
            return redirect("welcome_page")  # Change "home" to your desired page
    else:
        form = RegisterForm()
    return render(request, "registration_page/register.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def welcome_page(request):
    return render(request, 'welcome_page/index.html')


