from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.loginView, name='loginview'),
    path('register/', views.registerView, name='registerview'),
    path('logout/', views.logoutView, name='logout'),
    path('loginview/', views.login, name='login'),
    path('registerview/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('transaction/', views.user_transaction, name='user_transaction'),


    path('statistics_day/', views.statistics_day, name='statistics_day'),
    path('statistics_month/', views.statistics_month, name='statistics_month'),
    path('statistics_year/', views.statistics_year, name='statistics_year'),
    path('analyse/', views.analyse, name='analyse'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('create_billfold/', views.create_billfold, name='create_billfold'),
    path('create_new_billfold/', views.create_new_billfold, name='create_new_billfold'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('add_ratio/', views.add_ratio, name='add_ratio')
]
