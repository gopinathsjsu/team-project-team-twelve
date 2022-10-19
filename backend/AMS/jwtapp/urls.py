from django.urls import path,include

from jwtapp.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetView,UserPasswordResetView
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('userprofile/',UserProfileView.as_view(),name="profile"),
    path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
    path('send-reset-password-mail/',SendPasswordResetView.as_view(),name="sendresetpasswordmail"),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="sendresetpasswordmail"),

]

