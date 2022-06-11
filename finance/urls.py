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
    path('statistics/', views.statistics, name='statistics'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('create_billfold/', views.create_billfold, name='create_billfold'),
    path('create_new_billfold/', views.create_new_billfold, name='create_new_billfold'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
]
