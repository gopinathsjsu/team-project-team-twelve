from django.urls import path,include

from jwtapp.views import GetAllAirlineInfo, GetFlightSchedule, GetTerminalGateInfo, GetUserInfo, UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetView,UserPasswordResetView,ChangeGateStatus
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('userprofile/',UserProfileView.as_view(),name="profile"),
    path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
    path('send-reset-password-mail/',SendPasswordResetView.as_view(),name="sendresetpasswordmail"),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="sendresetpasswordmail"),
    # path('all-users/',UserListView.as_view(),name="allusers"),
    path('all-airline-info/',GetAllAirlineInfo.as_view(),name="allairlineinfo"),
    path('all-terminal-gate-info/',GetTerminalGateInfo.as_view(),name="allterminalgateinfo"),
    path('all-flight-schedule-info/',GetFlightSchedule.as_view(),name="allflightscheduleinfo"),
    path('user-info/<str:key>',GetUserInfo.as_view(),name="getspecificuserinfo"),
    path('gate-change/',ChangeGateStatus.as_view(),name="getspecificuserinfo"),
]


