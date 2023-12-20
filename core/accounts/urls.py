from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 
from .forms import StyledPasswordResetForm

urlpatterns = [
    path('', views.index_view, name='index'), 
    path('register', views.register_view, name='register'), 
    path('login', views.login_view, name='login'), 
    path('home', views.home_view, name='home'), 
    path('logout', views.logout_view, name='logout'), 
    path('editprofile', views.edit_profile_view, name='editprofile'), 
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html", form_class = StyledPasswordResetForm), name="reset_password"), 
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_mail_sent.html"), name="password_reset_done"), 
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"), 
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "registration/password_set_done.html"), name="password_reset_complete")

]
