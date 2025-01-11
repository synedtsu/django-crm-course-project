from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was error logging in. Please try again.")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

# def login_user():
#     pass

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Bravo!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})

def client_record(request, primary_key):
    if request.user.is_authenticated:
        client_record = Record.objects.get(id=primary_key)
        return render(request, 'record.html', {'client_record': client_record})
    else:
        messages.success(request, "You must be logged in to view records.")
        return redirect('home')
    
def delete_record(request, primary_key):
    if request.user.is_authenticated:
        delete_rec = Record.objects.get(id=primary_key)
        delete_rec.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete records")
        return redirect('home')