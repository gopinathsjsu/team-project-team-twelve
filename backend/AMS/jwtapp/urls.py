from django.urls import path,include

from jwtapp.views import GetAllAirlineInfo, GetFlightSchedule, GetTerminalGateInfo, GetUserInfo, UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetView,UserPasswordResetView,Terminal_RUD,AllTerminalGatesInfo,FlightScehduleRUD,FlightScehduleInfo,Airline_create,AirlineInfo,Airline_RUD,Terminal_create,FlightSchedule_create
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

    path('terminal-gate-create/',Terminal_create.as_view(),name="terminal-gate-create"),
    path('terminal-gate-rud/<str:pk>/',Terminal_RUD.as_view(),name="terminal-gate-rud"),
    path('terminal-gate-list/',AllTerminalGatesInfo.as_view(),name="terminal-gate-list"),

    path('flight-schedule-create/',FlightSchedule_create.as_view(),name="terminal-gate-create"),
    path('flight-schedule-rud/<str:pk>',FlightScehduleRUD.as_view(),name="flight-schedule-rud"),
    path('flight-schedule-list/',FlightScehduleInfo.as_view(),name="flight-schedule-list"),
    
    path('airline-create/',Airline_create.as_view(),name="airline-create"),
    path('airline-rud/<str:pk>',Airline_RUD.as_view(),name="airline-rud"),
    path('airline-list/',AirlineInfo.as_view(),name="airline-list")
]


