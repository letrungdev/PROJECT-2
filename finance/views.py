from django.shortcuts import render


def welcome(request):
    return render(request, 'welcome.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')

def statistics(request):
    return render(request, 'statistics.html')


def contact(request):
    return render(request, 'contact.html')


def profile(request):
    return render(request, 'profile.html')


