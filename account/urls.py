from django.urls import path, reverse
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name='main'),
    path('sign_up/', views.signup, name='sign_up'),
    path('login_page/', views.login_process, name='login_process'), # Create form page
    path('logout_process/', views.logout_process, name='logout_process'), # no html required
    path('delete_process/', views.delete_process, name='delete_process'), # no html required
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # Ajax
    path('load-cities/', views.load_cities, name='load_cities'),
    path('load-zips/', views.load_zips, name='load_zips'),



    # Password change, when you know your old password
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"),
         name="password_change"),  # Create form page in password_change.html, by default form is passed

    path('password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),
         name="password_change_done"),  # Create Confirm message, also shows a link to go anywhere (put your app on top)



    # Password reset. when you forget the password
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name="reset_password"),  # Create form page, by default form is there.

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name="password_reset_done"), # a simple html to show an email is sent, no need to create any view



    # r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"),
         name="password_reset_confirm"),
    # Two process are done
    # 1. An email sent {{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
    # 2. After clicking on email, this html is shown which contains a form

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_complete"),
    # message showing password reset is completed, also shows a link to go anywhere

]
