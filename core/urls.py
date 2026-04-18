from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('' , index , name='index'),
    path('menu/', menu , name='menu'),
    path('about/', about , name='about'),
    path('services/', services , name='services'),
    path('contact/', contact , name='contact'),
    path('testemonial/', testemonial , name='testemonial'),
    path('privacy/', privacy , name='privacy'),
    path('term/', term , name='term'),
    #auth
    path('register/',register, name='register'),
    path('login/',log_in, name='login'),
    path('logout/',log_out, name='logout'),
    path('change_password/',change_password, name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
    
]
