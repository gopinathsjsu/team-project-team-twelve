from django.urls import path,include

from jwtapp.views import GetUserInfo, UserRegistrationView,UserLoginView,UserChangePasswordView,SendPasswordResetView,UserPasswordResetView,Terminal_RUD,AllTerminalGatesInfo,FlightScehduleRUD,FlightScehduleInfo,Airline_create,AirlineInfo,Airline_RUD,Terminal_create,FlightSchedule_create, Airline_create, Airline_RUD, AirlineInfo, Passenger_create, PassengerRUD, PassengerInfo
urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
    path('send-reset-password-mail/',SendPasswordResetView.as_view(),name="sendresetpasswordmail"),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="sendresetpasswordmail"),
    path('user-info/<str:key>',GetUserInfo.as_view(),name="getspecificuserinfo"),

    path('terminal-gate-create/',Terminal_create.as_view(),name="terminal-gate-create"),
    path('terminal-gate-rud/<str:pk>/',Terminal_RUD.as_view(),name="terminal-gate-rud"),
    path('terminal-gate-list/',AllTerminalGatesInfo.as_view(),name="terminal-gate-list"),

    path('flight-schedule-create/',FlightSchedule_create.as_view(),name="terminal-gate-create"),
    path('flight-schedule-rud/<str:pk>',FlightScehduleRUD.as_view(),name="flight-schedule-rud"),
    path('flight-schedule-list/',FlightScehduleInfo.as_view(),name="flight-schedule-list"),
    
    path('airline-create/',Airline_create.as_view(),name="airline-create"),
    path('airline-rud/<str:pk>',Airline_RUD.as_view(),name="airline-rud"),
    path('airline-list/',AirlineInfo.as_view(),name="airline-list"),

    path('airline-main-create/',Airline_create.as_view(),name="airline-main-create"),
    path('airline-main-rud/<str:pk>',Airline_RUD.as_view(),name="airline-main-rud"),
    path('airline-main-list/',AirlineInfo.as_view(),name="airline-main-list"),

    path('flight-passenger-create/',Passenger_create.as_view(),name="flight-passenger-create"),
    path('flight-passenger-rud/<str:pk>',PassengerRUD.as_view(),name="flight-passenger-rud"),
    path('flight-passenger-list/',PassengerInfo.as_view(),name="flight-passenger-list")
]


