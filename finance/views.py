from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import Billfold, Transaction, Expenditureplan, Analysis


def welcome(request):
    return render(request, 'welcome.html')


def loginView(request):
    return render(request, 'login.html')


def registerView(request):
    return render(request, 'register.html')


def logoutView(request):
    logout(request)
    return redirect('loginview')


@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            user_has_bill = Billfold.objects.values_list('user', flat=True)
            if username in user_has_bill:
                return redirect('dashboard')
            else:
                return redirect('create_billfold')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('loginview')


@csrf_protect
def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)
        a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        a.save()
        messages.success(request, 'Account was created successfully')
        return redirect('loginview')


def dashboard(request):
    user = request.user
    billfold = Billfold.objects.get(user=user)
    balance = billfold.balance
    currency_unit = billfold.currency_unit[-2]
    fullname = user.first_name + ' ' + user.last_name
    name = user.first_name
    return render(request, 'dashboard.html', {'fullname': fullname, 'name': name, 'balance': balance, 'currency_unit': currency_unit})


def statistics(request):
    user = request.user
    fullname = user.first_name + ' ' + user.last_name
    name = user.first_name
    return render(request, 'statistics.html', {'fullname': fullname, 'name': name})


def contact(request):
    user = request.user
    fullname = user.first_name + ' ' + user.last_name
    name = user.first_name
    return render(request, 'contact.html', {'fullname': fullname, 'name': name})


def profile(request):
    user = request.user
    fullname = user.first_name + ' ' + user.last_name
    name = user.first_name
    return render(request, 'profile.html', {'fullname': fullname, 'name': name})


def create_billfold(request):
    user = request.user
    fullname = user.first_name + ' ' + user.last_name
    name = user.first_name
    return render(request, 'create_billfold.html', {'fullname': fullname, 'name': name})


def create_new_billfold(request):
    user = request.user
    currency_unit = request.POST['currency_unit']
    billfold_name = request.POST['billfold_name']
    balance = request.POST['balance']
    billfold = Billfold(user=user, currency_unit=currency_unit, billfold_name=billfold_name, balance=balance)
    billfold.save()
    return redirect('dashboard')


def add_transaction(request):
    if request.method == 'POST':
        user = request.user.username
        amount = request.POST['amount']
        category = request.POST['category']
        note = request.POST['note']
        tran_time = request.POST['tran_time']
        tran_image = request.POST['tran_image']
        a = Transaction(user=user, amount=amount, category=category, note=note, tran_time=tran_time, tran_image=tran_image)
        a.save()
        return redirect('dashboard')

