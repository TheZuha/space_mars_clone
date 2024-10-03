from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required


# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        return redirect('category_list')

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = CustomUser.objects.create(username=username)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserForm()

    return render(request, 'register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            message = "Invalid username or password"
            form = AuthenticationForm()
            return render(request, 'login.html', {'form': form, 'message': message})

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
