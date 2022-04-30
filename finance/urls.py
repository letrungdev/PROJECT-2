from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('statistics/', views.statistics, name='statistics'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile')
]