from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import Billfold, Transaction, Expenditureplan, Analysis, Track
from datetime import datetime


def welcome(request):
    return render(request, 'index.html')


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
    inflow_today = 0
    outflow_today = 0
    inflow_month = 0
    outflow_month = 0
    inflow_year = 0
    outflow_year = 0
    today = ''

    data_income = []
    data_outcome = []
    data_total = []
    categories = []

    user = request.user
    billfold = Billfold.objects.get(user=user)
    last_track = Track.objects.filter(user=user).latest('time_track')
    total = last_track.balance
    currency_unit = billfold.currency_unit[-2]
    fullname = user.first_name + ' ' + user.last_name
    name = user.first_name
    tracks = Track.objects.filter(user=user)
    time_check = datetime.now().strftime("%Y-%m-%d")
    transactions = Transaction.objects.filter(user=user, tran_time__startswith=time_check)
    for track in tracks:
        # Day track
        today = str(track.time_track).split(' ')[0]
        month = str(track.time_track).split(' ')[0][0:8]
        year = str(track.time_track).split(' ')[0][0:5]
        if today == datetime.now().strftime("%Y-%m-%d"):
            if track.inflow == '0':
                outflow_today += int(track.outflow)
                data_outcome.append(track.outflow)
            else:
                inflow_today += int(track.inflow)
                data_income.append(track.inflow)
            data_total.append(track.balance)
            categories.append("\"" + track.time_track + "Z\"")

        # Month track
        if month == datetime.now().strftime("%Y-%m"):
            if track.inflow == '0':
                outflow_month += int(track.outflow)
            else:
                inflow_month += int(track.inflow)
        # Year track
        if year == datetime.now().strftime("%Y"):
            if track.inflow == '0':
                outflow_year += int(track.outflow)
            else:
                inflow_year += int(track.inflow)

    return render(request,
                  'dashboard.html',
                  {'fullname': fullname,
                   'name': name,
                   'today': today,
                   'total': total,
                   'data_income': data_income,
                   'data_outcome': data_outcome,
                   'data_total': data_total,
                   'categories': categories,
                   'currency_unit': currency_unit,
                   'inflow_today': inflow_today,
                   'outflow_today': outflow_today,
                   'inflow_month': inflow_month,
                   'outflow_month': outflow_month,
                   'inflow_year': inflow_year,
                   'outflow_year': outflow_year,
                   'transactions': transactions,
                   }
                  )


def statistics(request):
    necessary = ["Food & Drink", "Transportation", "Rentals", "Water & Electricity",
                 "Internet", "Household Utensils", "Family Payments"]
    self_improvement = ["Education", "Gym & Fitness", "Medical Check-up"]
    long_term = ["Saving Money"]
    investing = ["Investing"]
    play = ["Online Services", "Relax Services"]
    give = ["Charity Organization", "Help Acquaintance", "Help Stranger"]

    nec_value = 0
    sel_value = 0
    lon_value = 0
    inv_value = 0
    pla_value = 0
    giv_value = 0

    user = request.user
    time_check = datetime.now().strftime("%Y-%m-%d")
    transactions = Transaction.objects.filter(user=user, tran_time__startswith=time_check)
    for transaction in transactions:
        if transaction.category in necessary:
            nec_value += int(transaction.amount)
        elif transaction.category in self_improvement:
            sel_value += int(transaction.amount)
        elif transaction.category in long_term:
            lon_value += int(transaction.amount)
        elif transaction.category in investing:
            inv_value += int(transaction.amount)
        elif transaction.category in play:
            pla_value += int(transaction.amount)
        elif transaction.category in give:
            giv_value += int(transaction.amount)

    nec_expense = {
        'value': nec_value,
        'name': 'Necessary'
    }
    sel_expense = {
        'value': sel_value,
        'name': 'Self Improvement'
    }
    lon_expense = {
        'value': lon_value,
        'name': 'Long-term Saving'
    }
    inv_expense = {
        'value': inv_value,
        'name': 'Investing'
    }
    pla_expense = {
        'value': pla_value,
        'name': 'Play & Relax'
    }
    giv_expense = {
        'value': giv_value,
        'name': 'Give Away'
    }
    data = [nec_expense, sel_expense, lon_expense, inv_expense, pla_expense, giv_expense]
    user = request.user
    fullname = user.first_name + ' ' + user.last_name
    name = user.first_name
    return render(request, 'statistics.html',
                  {'fullname': fullname,
                   'name': name,
                   'data': data,
                   }
                  )


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
    time_track = datetime.now().strftime("%Y-%m-%d %H:%M")
    track = Track(user=user, billfold=billfold_name, inflow=0, outflow=0, balance=balance, time_track=time_track)
    track.save()
    return redirect('dashboard')


def add_transaction(request):
    positive_categories = ['Salary', 'Bonus', 'Other Income']
    if request.method == 'POST':
        inflow = ''
        outflow = ''
        user = request.user.username
        amount = request.POST['amount']
        category = request.POST['category']
        note = request.POST['note']
        tran_time = request.POST['tran_time'].replace('T', ' ')
        tran_image = request.POST['tran_image']
        if category in positive_categories:
            type = '+'
        else:
            type = '-'
        a = Transaction(user=user, amount=amount, category=category, type=type, note=note, tran_time=tran_time,
                        tran_image=tran_image)
        a.save()
        track_before = Track.objects.filter(user=user).latest('time_track')
        balance = track_before.balance
        billfold = track_before.billfold
        if type == '+':
            inflow = amount
            outflow = 0
            balance = str(int(balance) + int(inflow))
        elif type == '-':
            inflow = 0
            outflow = amount
            balance = str(int(balance) - int(outflow))
        track = Track(user=user, billfold=billfold, balance=balance, inflow=inflow, outflow=outflow, time_track=tran_time)
        track.save()
        return redirect('dashboard')

