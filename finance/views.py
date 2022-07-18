from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from .models import Billfold, Transaction, Analysis, Track
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from . forms import TransactionForm


# category expenses
labels1 = ['Necessary', 'Self Improvement', 'Long-term Saving', 'Investing', 'Play & Relax', 'Give Away']
necessary = ["Food & Drink", "Transportation", "Rentals", "Water & Electricity",
             "Internet", "Household Utensils", "Family Payments"]
self_improvement = ["Education", "Gym & Fitness", "Medical Check-up"]
long_term = ["Saving Money"]
investing = ["Investing"]
play = ["Online Services", "Relax Services"]
give = ["Charity Organization", "Help Acquaintance", "Help Stranger"]
income = ["Salary", "Bonus", "Other Income"]
money_name = ['necessary', 'self_improvement', 'long-term savings', 'investing', 'play & relax', 'give away']


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
            messages.warning(request, "Invalid username or password")
            return redirect('loginview')


@csrf_protect
def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if password != repassword:
            messages.error(request, 'Your password and confirmation password do not match.')
            return redirect('registerview')
        else:
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
    data_total_day = []
    data_total_month = []
    data_total_year = []
    categories_day = []
    categories_month = []
    categories_year = []

    user = request.user
    billfold = Billfold.objects.get(user=user)
    currency_unit = billfold.currency_unit[-2]

    last_track = Track.objects.filter(user=user).latest('time_track')
    total = last_track.balance

    tracks = Track.objects.filter(user=user).order_by('time_track')
    time_check = datetime.now().strftime("%Y-%m-%d")
    transactions = Transaction.objects.filter(user=user, tran_time__startswith=time_check)

    for track in tracks:
        # Day track
        today = str(track.time_track).split(' ')[0]
        month = str(track.time_track).split(' ')[0][0:7]
        year = str(track.time_track).split(' ')[0][0:4]
        if today != time_check:
            if '00:00' not in categories_day:
                data_total_day.append(track.balance)
                categories_day.append('00:00')
            else:
                data_total_day[0] = track.balance
        else:
            if track.inflow == '0':
                outflow_today += int(track.outflow)
                data_outcome.append(track.outflow)
            else:
                inflow_today += int(track.inflow)
                data_income.append(track.inflow)
            data_total_day.append(track.balance)
            categories_day.append(str(track.time_track).split(' ')[1])

        # Month track
        if month == datetime.now().strftime("%Y-%m"):
            day_in_month = str(track.time_track).split(' ')[0][5:]
            if day_in_month not in categories_month:
                data_total_month.append(track.balance)
                categories_month.append(day_in_month)
            else:
                for index, n in enumerate(categories_month):
                    if day_in_month == n:
                        data_total_month[index] = track.balance

            if track.inflow == '0':
                outflow_month += int(track.outflow)
            else:
                inflow_month += int(track.inflow)
        if year == datetime.now().strftime("%Y"):
            if track.inflow == '0':
                outflow_year += int(track.outflow)
            else:
                inflow_year += int(track.inflow)

    return render(request,
                  'dashboard.html',
                  {
                   'today': today,
                   'total': total,
                   'data_income': data_income,
                   'data_outcome': data_outcome,
                   'data_total_day': data_total_day,
                   'data_total_month': data_total_month,
                   'data_total_year': data_total_year,
                   'categories_day': categories_day,
                   'categories_month': categories_month,
                   'categories_year': categories_year,
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


@login_required
def user_transaction(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-tran_time')
    count = transactions.count()
    return render(request, 'transaction.html', {'transactions': transactions, 'count': count})


def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'edit_transaction.html', {'transaction': transaction})


def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    form = TransactionForm(request.POST, instance=transaction)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated Successfully!")
    return redirect('user_transaction')


def statistics_day(request):
    # day check
    nec_value_day = 0
    sel_value_day = 0
    lon_value_day = 0
    inv_value_day = 0
    pla_value_day = 0
    giv_value_day = 0
    user = request.user

    day_check = datetime.now().strftime("%Y-%m-%d")
    transactions = Transaction.objects.filter(user=user, tran_time__startswith=day_check)
    necessary_trans = Transaction.objects.filter(user=user, tran_time__startswith=day_check, kind='Necessary')
    self_improvement_trans = Transaction.objects.filter(user=user, tran_time__startswith=day_check, kind='Self Improvement')
    long_term_trans = Transaction.objects.filter(user=user, tran_time__startswith=day_check, kind='Long-term Savings')
    investing_trans = Transaction.objects.filter(user=user, tran_time__startswith=day_check, kind='Investing')
    play_trans = Transaction.objects.filter(user=user, tran_time__startswith=day_check, kind='Play & Relax')
    give_trans = Transaction.objects.filter(user=user, tran_time__startswith=day_check, kind='Give Away')
    income_trans = Transaction.objects.filter(user=user, tran_time__startswith=day_check, kind='Income')

    for transaction in transactions:
        if transaction.category in necessary:
            nec_value_day += transaction.amount
        elif transaction.category in self_improvement:
            sel_value_day += transaction.amount
        elif transaction.category in long_term:
            lon_value_day += transaction.amount
        elif transaction.category in investing:
            inv_value_day += transaction.amount
        elif transaction.category in play:
            pla_value_day += transaction.amount
        elif transaction.category in give:
            giv_value_day += transaction.amount
    data_day = [nec_value_day, sel_value_day, lon_value_day, inv_value_day, pla_value_day, giv_value_day]

    return render(request, 'statistics/today.html',
                  {
                    'labels1': labels1,
                    'data_day': data_day,
                    'necessary_trans': necessary_trans,
                    'self_improvement_trans': self_improvement_trans,
                    'long_term_trans': long_term_trans,
                    'investing_trans': investing_trans,
                    'play_trans': play_trans,
                    'give_trans': give_trans,
                    'income_trans': income_trans
                   }
                  )


def statistics_month(request):
    avg_months = []
    dates = []
    necessary_dates = []
    self_improvement_dates = []
    long_term_dates = []
    investing_dates = []
    play_dates = []
    give_dates = []
    date_index = 0
    # month check
    nec_value_month = 0
    sel_value_month = 0
    lon_value_month = 0
    inv_value_month = 0
    pla_value_month = 0
    giv_value_month = 0

    nec_value_last_month = 0
    sel_value_last_month = 0
    lon_value_last_month = 0
    inv_value_last_month = 0
    pla_value_last_month = 0
    giv_value_last_month = 0

    nec_value_month_avg = 0
    sel_value_month_avg = 0
    lon_value_month_avg = 0
    inv_value_month_avg = 0
    pla_value_month_avg = 0
    giv_value_month_avg = 0

    data_month_avg = []
    user = request.user
    month_check = datetime.now().strftime("%Y-%m")
    year_check = datetime.now().strftime("%Y")

    last_month = (date.today().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
    last_month_transactions = Transaction.objects.filter(user=user, tran_time__startswith=last_month)
    for transaction in last_month_transactions:
        if transaction.category in necessary:
            nec_value_last_month += transaction.amount
        elif transaction.category in self_improvement:
            sel_value_last_month += transaction.amount
        elif transaction.category in long_term:
            lon_value_last_month += transaction.amount
        elif transaction.category in investing:
            inv_value_last_month += transaction.amount
        elif transaction.category in play:
            pla_value_last_month += transaction.amount
        elif transaction.category in give:
            giv_value_last_month += transaction.amount
    data_last_month = [nec_value_last_month, sel_value_last_month, lon_value_last_month, inv_value_last_month, pla_value_last_month, giv_value_last_month]
    if data_last_month == [0]*6:
        data_last_month = None

    average_transactions = Transaction.objects.filter(user=user, tran_time__startswith=year_check).exclude(tran_time__startswith=month_check)
    for transaction in average_transactions:
        a = transaction.tran_time[5:7]
        if a not in avg_months:
            avg_months.append(a)
        if transaction.category in necessary:
            nec_value_month_avg += transaction.amount
        elif transaction.category in self_improvement:
            sel_value_month_avg += transaction.amount
        elif transaction.category in long_term:
            lon_value_month_avg += transaction.amount
        elif transaction.category in investing:
            inv_value_month_avg += transaction.amount
        elif transaction.category in play:
            pla_value_month_avg += transaction.amount
        elif transaction.category in give:
            giv_value_month_avg += transaction.amount
    x = len(avg_months)
    if x > 0:
        data_month_avg = [nec_value_month_avg/x, sel_value_month_avg/x, lon_value_month_avg/x, inv_value_month_avg/x, pla_value_month_avg/x, giv_value_month_avg/x]
        if data_month_avg == [0]*6:
            data_month_avg = None

    transactions = Transaction.objects.filter(user=user, tran_time__startswith=month_check).exclude(type='+')
    for transaction in transactions:
        if transaction.category in necessary:
            nec_value_month += transaction.amount
        elif transaction.category in self_improvement:
            sel_value_month += transaction.amount
        elif transaction.category in long_term:
            lon_value_month += transaction.amount
        elif transaction.category in investing:
            inv_value_month += transaction.amount
        elif transaction.category in play:
            pla_value_month += transaction.amount
        elif transaction.category in give:
            giv_value_month += transaction.amount

        month_date = transaction.tran_time[5:10]
        if month_date not in dates:
            dates.append(month_date)

        for n, datee in enumerate(dates):
            if month_date == datee:
                date_index = n

        if transaction.kind == 'Necessary':
            length = len(necessary_dates)
            if length <= date_index:
                for _ in range(len(range(date_index)) - length):
                    necessary_dates.append(0)
                necessary_dates.append(transaction.amount)
            else:
                necessary_dates[date_index] += transaction.amount
        elif transaction.kind == 'Self Improvement':
            length = len(self_improvement_dates)
            if length <= date_index:
                for _ in range(len(range(date_index)) - length):
                    self_improvement_dates.append(0)
                self_improvement_dates.append(transaction.amount)
            else:
                self_improvement_dates[date_index] += transaction.amount

        elif transaction.kind == 'Long-term Savings':
            length = len(long_term_dates)
            if length <= date_index:
                for _ in range(len(range(date_index)) - length):
                    necessary_dates.append(0)
                long_term_dates.append(transaction.amount)
            else:
                long_term_dates[date_index] += transaction.amount

        elif transaction.kind == 'Investing':
            length = len(investing_dates)
            if length <= date_index:
                for _ in range(len(range(date_index)) - length):
                    investing_dates.append(0)
                investing_dates.append(transaction.amount)
            else:
                investing_dates[date_index] += transaction.amount

        elif transaction.kind == 'Play & Relax':
            length = len(play_dates)
            if length <= date_index:
                for _ in range(len(range(date_index)) - length):
                    play_dates.append(0)
                play_dates.append(transaction.amount)
            else:
                play_dates[date_index] += transaction.amount

        elif transaction.kind == 'Give Away':
            length = len(give_dates)
            if length <= date_index:
                for _ in range(len(range(date_index)) - length):
                    give_dates.append(0)
                give_dates.append(transaction.amount)
            else:
                give_dates[date_index] += transaction.amount
    data_month = [nec_value_month, sel_value_month, lon_value_month, inv_value_month, pla_value_month, giv_value_month]

    top_incomes = Transaction.objects.filter(user=user, type='+', tran_time__startswith=month_check).order_by('-amount')[:3]
    top_outcomes = Transaction.objects.filter(user=user, type='-', tran_time__startswith=month_check).order_by('-amount')[:3]
    return render(request, 'statistics/month.html',
                  {
                   'labels1': labels1,
                   'data_month': data_month,
                   'data_last_month': data_last_month,
                   'data_month_avg': data_month_avg,
                   'dates': dates,
                   'necessary_dates': necessary_dates,
                   'self_improvement_dates': self_improvement_dates,
                   'long_term_dates': long_term_dates,
                   'investing_dates': investing_dates,
                   'play_dates': play_dates,
                   'give_dates': give_dates,
                   'top_incomes': top_incomes,
                   'top_outcomes': top_outcomes
                   }
                  )


def statistics_year(request):
    user = request.user
    necessary_months = [0]*12
    self_improvement_months = [0]*12
    long_term_months = [0]*12
    investing_months = [0]*12
    play_months = [0]*12
    give_months = [0]*12
    inflow_months = [0]*12
    outflow_months = [0]*12

    nec_value_year = 0
    nec_value_last_year = 0
    nec_value_avg = 0
    sel_value_year = 0
    sel_value_last_year = 0
    sel_value_avg = 0
    lon_value_year = 0
    lon_value_last_year = 0
    lon_value_avg = 0
    inv_value_year = 0
    inv_value_last_year = 0
    inv_value_avg = 0
    pla_value_year = 0
    pla_value_last_year = 0
    pla_value_avg = 0
    giv_value_year = 0
    giv_value_last_year = 0
    giv_value_avg = 0
    avg_years = []
    data_year_avg = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year_check = datetime.now().strftime("%Y")
    tracks = Track.objects.filter(user=user)
    for track in tracks:
        if year_check in track.time_track:
            month_number = int(track.time_track[5:7]) - 1
            inflow_months[month_number] += int(track.inflow)
            outflow_months[month_number] += int(track.outflow)

    last_year = int(int(year_check) - 1)
    last_year_transactions = Transaction.objects.filter(user=user, tran_time__startswith=last_year)
    for transaction in last_year_transactions:
        if transaction.category in necessary:
            nec_value_last_year += transaction.amount
        elif transaction.category in self_improvement:
            sel_value_last_year += transaction.amount
        elif transaction.category in long_term:
            lon_value_last_year += transaction.amount
        elif transaction.category in investing:
            inv_value_last_year += transaction.amount
        elif transaction.category in play:
            pla_value_last_year += transaction.amount
        elif transaction.category in give:
            giv_value_last_year += transaction.amount
    data_last_year = [nec_value_last_year, sel_value_last_year, lon_value_last_year, inv_value_last_year, pla_value_last_year, giv_value_last_year]
    if data_last_year == [0]*6:
        data_last_year = None
    average_transactions = Transaction.objects.filter(user=user).exclude(tran_time__startswith=year_check)
    for transaction in average_transactions:
        a = transaction.tran_time[0:4]
        if a not in avg_years:
            avg_years.append(a)
        if transaction.category in necessary:
            nec_value_avg += transaction.amount
        elif transaction.category in self_improvement:
            sel_value_avg += transaction.amount
        elif transaction.category in long_term:
            lon_value_avg += transaction.amount
        elif transaction.category in investing:
            inv_value_avg += transaction.amount
        elif transaction.category in play:
            pla_value_avg += transaction.amount
        elif transaction.category in give:
            giv_value_avg += transaction.amount
    x = len(avg_years)
    if x > 0:
        data_year_avg = [nec_value_avg/x, sel_value_avg/x, lon_value_avg/x, inv_value_avg/x, pla_value_avg/x, giv_value_avg/x]
    else:
        data_year_avg = None

    transactions = Transaction.objects.filter(user=user, tran_time__startswith=year_check).exclude(type='+')
    for transaction in transactions:
        if transaction.category in necessary:
            nec_value_year += transaction.amount
        elif transaction.category in self_improvement:
            sel_value_year += transaction.amount
        elif transaction.category in long_term:
            lon_value_year += transaction.amount
        elif transaction.category in investing:
            inv_value_year += transaction.amount
        elif transaction.category in play:
            pla_value_year += transaction.amount
        elif transaction.category in give:
            giv_value_year += transaction.amount

        month_index = int(transaction.tran_time[5:7]) - 1
        if transaction.kind == 'Necessary':
            necessary_months[month_index] += transaction.amount
        elif transaction.kind == 'Self Improvement':
            self_improvement_months[month_index] += transaction.amount
        elif transaction.kind == 'Long-term Savings':
            long_term_months[month_index] += transaction.amount
        elif transaction.kind == 'Investing':
            investing_months[month_index] += transaction.amount
        elif transaction.kind == 'Play & Relax':
            play_months[month_index] += transaction.amount
        elif transaction.kind == 'Give Away':
            give_months[month_index] += transaction.amount
    data_year = [nec_value_year, sel_value_year, lon_value_year, inv_value_year, pla_value_year, giv_value_year]

    top_incomes = Transaction.objects.filter(user=user, type='+', tran_time__startswith=year_check).order_by('-amount')[:3]
    top_outcomes = Transaction.objects.filter(user=user, type='-', tran_time__startswith=year_check).order_by('-amount')[:3]
    return render(request, 'statistics/year.html',
                  {
                      'labels1': labels1,
                      'data_year': data_year,
                      'months': months,
                      'inflow_months': inflow_months,
                      'outflow_months': outflow_months,
                      'necessary_months': necessary_months,
                      'self_improvement_months': self_improvement_months,
                      'investing_months': investing_months,
                      'play_months': play_months,
                      'give_months': give_months,
                      'long_term_months': long_term_months,
                      'top_incomes': top_incomes,
                      'top_outcomes': top_outcomes,
                      'data_last_year': data_last_year,
                      'data_year_avg': data_year_avg,
                  }
                  )


def analyse(request):
    income_money = 0
    nec_money = 0
    sel_money = 0
    lon_money = 0
    inv_money = 0
    pla_money = 0
    giv_money = 0

    nec_ideal = 0
    nec_rest = 0
    nec_percent = 0
    sel_ideal = 0
    sel_rest = 0
    sel_percent = 0
    lon_ideal = 0
    lon_rest = 0
    lon_percent = 0
    inv_ideal = 0
    inv_rest = 0
    inv_percent = 0
    pla_ideal = 0
    pla_rest = 0
    pla_percent = 0
    giv_ideal = 0
    giv_rest = 0
    giv_percent = 0

    ideal = []
    expense = []
    interval = []
    user = request.user
    billfold = Billfold.objects.get(user=user)
    currency = billfold.currency_unit.split('(')[1].replace(')', '')

    month = datetime.now().strftime("%Y-%m")
    first_day = date.today().replace(day=1)
    last_month = ''
    last_2_month = ''
    start = ''
    end = ''
    analysis = Analysis.objects.filter(user=user).order_by('-id')

    if len(analysis) > 0:
        ratios = analysis[0].ratio.split(' ')
        necessary_ratio = float(ratios[0])
        self_improvement_ratio = float(ratios[1])
        long_term_ratio = float(ratios[2])
        investing_ratio = float(ratios[3])
        play_ratio = float(ratios[4])
        give_ratio = float(ratios[5])
        interval = analysis[0].interval
        if interval == '2':
            interval = '2 months'
            last_month = (first_day - relativedelta(months=1)).strftime('%Y-%m')
            last_month_trans = Transaction.objects.filter(user=user, tran_time__startswith=last_month)
            this_month_trans = Transaction.objects.filter(user=user, tran_time__startswith=month)
            transactions = this_month_trans.union(last_month_trans)
        elif interval == '3':
            interval = '3 months'
            last_month = (first_day - relativedelta(months=1)).strftime('%Y-%m')
            last_month_trans = Transaction.objects.filter(user=user, tran_time__startswith=last_month)
            last_2_month = (first_day - relativedelta(months=2)).strftime('%Y-%m')
            last_2_month_trans = Transaction.objects.filter(user=user, tran_time__startswith=last_2_month)
            this_month_trans = Transaction.objects.filter(user=user, tran_time__startswith=month)
            transactions = this_month_trans.union(last_month_trans).union(last_2_month_trans)
        elif ' ' in interval:
            start = interval.split(' ')[0]
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end = interval.split(' ')[1]
            end_date = datetime.strptime(end, "%Y-%m-%d").date() + timedelta(days=1)
            transactions = Transaction.objects.filter(user=user, tran_time__range=(start_date, end_date))
        else:
            interval = '1 month'
            transactions = Transaction.objects.filter(user=user, tran_time__startswith=month)
    else:
        interval = '1 month'
        necessary_ratio = 0.55
        self_improvement_ratio = 0.1
        long_term_ratio = 0.1
        investing_ratio = 0.1
        play_ratio = 0.1
        give_ratio = 0.05
        transactions = Transaction.objects.filter(user=user, tran_time__startswith=month)

    for transaction in transactions:
        if transaction.category in necessary:
            nec_money += transaction.amount
        elif transaction.category in self_improvement:
            sel_money += transaction.amount
        elif transaction.category in long_term:
            lon_money += transaction.amount
        elif transaction.category in investing:
            inv_money += transaction.amount
        elif transaction.category in play:
            pla_money += transaction.amount
        elif transaction.category in give:
            giv_money += transaction.amount
        elif transaction.category in income:
            income_money += transaction.amount
    expense.append(nec_money)
    expense.append(sel_money)
    expense.append(lon_money)
    expense.append(inv_money)
    expense.append(pla_money)
    expense.append(giv_money)

    if income_money > 0:
        nec_ideal = int(necessary_ratio * income_money)
        ideal.append(nec_ideal)
        sel_ideal = int(self_improvement_ratio * income_money)
        ideal.append(sel_ideal)
        lon_ideal = int(long_term_ratio * income_money)
        ideal.append(lon_ideal)
        inv_ideal = int(investing_ratio * income_money)
        ideal.append(inv_ideal)
        pla_ideal = int(play_ratio * income_money)
        ideal.append(pla_ideal)
        giv_ideal = int(give_ratio * income_money)
        ideal.append(giv_ideal)

        nec_rest = int(nec_ideal - nec_money)
        nec_percent = nec_money / income_money

        sel_rest = int(sel_ideal - sel_money)
        sel_percent = sel_money / income_money

        lon_rest = int(lon_ideal - lon_money)
        lon_percent = lon_money / income_money

        inv_rest = int(inv_ideal - inv_money)
        inv_percent = inv_money / income_money

        pla_rest = int(pla_ideal - pla_money)
        pla_percent = pla_money / income_money

        giv_rest = int(giv_ideal - giv_money)
        giv_percent = giv_money / income_money

    percent = [necessary_ratio, self_improvement_ratio, long_term_ratio, investing_ratio, play_ratio, give_ratio]
    spent = [nec_money, sel_money, lon_money, inv_money, pla_money, giv_money]
    len_trans = len(transactions)
    return render(request, 'analyse.html', {
        'nec_money': nec_money,
        'nec_ideal': nec_ideal,
        'nec_rest': nec_rest,
        'nec_percent': nec_percent,

        'sel_money': sel_money,
        'sel_ideal': sel_ideal,
        'sel_rest': sel_rest,
        'sel_percent': sel_percent,

        'lon_money': lon_money,
        'lon_ideal': lon_ideal,
        'lon_rest': lon_rest,
        'lon_percent': lon_percent,

        'inv_money': inv_money,
        'inv_ideal': inv_ideal,
        'inv_rest': inv_rest,
        'inv_percent': inv_percent,

        'pla_money': pla_money,
        'pla_ideal': pla_ideal,
        'pla_rest': pla_rest,
        'pla_percent': pla_percent,

        'giv_money': giv_money,
        'giv_ideal': giv_ideal,
        'giv_rest': giv_rest,
        'giv_percent': giv_percent,

        'expense': expense,
        'ideal': ideal,
        'money_name': money_name,
        'percent': percent,
        'currency': currency,
        'interval': interval,
        'last_month': last_month,
        'last_2_month': last_2_month,
        'month': month,
        'start': start,
        'end': end,
        'len_trans': len_trans,
        'labels1': labels1,
        'spent': spent
    })


def contact(request):
    return render(request, 'contact.html')


def profile(request):
    return render(request, 'profile.html')


def create_billfold(request):
    return render(request, 'create_billfold.html')


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
        kind = ''
        user = request.user.username
        amount = request.POST['amount']
        category = request.POST['category']
        if category in necessary:
            kind = 'Necessary'
        if category in self_improvement:
            kind = 'Self Improvement'
        if category in long_term:
            kind = 'Long-term Savings'
        if category in investing:
            kind = 'Investing'
        if category in play:
            kind = 'Play & Relax'
        if category in give:
            kind = 'Give Away'
        if category in income:
            kind = 'Income'
        note = request.POST['note']
        tran_time = request.POST['tran_time'].replace('T', ' ')
        tran_image = request.POST['tran_image']
        if category in positive_categories:
            type = '+'
        else:
            type = '-'
        a = Transaction(user=user, amount=amount, category=category, kind=kind, type=type, note=note, tran_time=tran_time,
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


def add_ratio(request):
    if request.method == 'POST':
        user = request.user.username
        interval = request.POST.get('interval', False)
        if not interval:
            interval = request.POST['start'] + ' ' + request.POST['end']

        necessary_ratio = request.POST['necessary']
        self_improvement_ratio = request.POST['self_improvement']
        long_term_ratio = request.POST['long_term']
        investing_ratio = request.POST['investing']
        play_ratio = request.POST['play']
        give_ratio = request.POST['give']

        ratio = necessary_ratio + ' ' + self_improvement_ratio + ' ' + long_term_ratio + ' ' + investing_ratio + ' ' + play_ratio + ' ' + give_ratio
        a = Analysis(user=user, interval=interval, ratio=ratio)
        a.save()
        return redirect('analyse')
