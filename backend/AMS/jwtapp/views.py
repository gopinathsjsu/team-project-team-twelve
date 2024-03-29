from multiprocessing import context
from django.shortcuts import render
from jwtapp.models import Mio_airline, Mio_flight_schedule, Mio_terminal, User, Mio_passenger,BaggageCar
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from jwtapp.permissions import adminpermission,airline_employee_permission,airport_employee_permission
from jwtapp.serializers import MioAirlineSerializer, MioFlightScheduleSerializer, MioTerminalSerializer, UserRegistrationSerializer, MioPassengerSerializer
from jwtapp.serializers import UserLoginSerializer
from jwtapp.renderers import UserRenderer
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer

# Create your views here.

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from jwtapp.serializers import UserProfileSerializer
from jwtapp.serializers import UserChangePasswordSerializer
from jwtapp.serializers import SendPasswordResetEmailSerializer
from jwtapp.serializers import UserPasswordResetSerializer,BaggageSerializer
from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,UpdateModelMixin,RetrieveModelMixin

from django.core.exceptions import ValidationError
import uuid
import datetime


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    # renderer_classes=[UserRenderer]
    # permission_classes=[adminpermission]
    def post(self, request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        if serializer.is_valid():
            user=serializer.save()
            # generate token when user get saved:
            token=get_tokens_for_user(user)
            # return Response({"token":token,"msg":"Registration successful","status":status.HTTP_201_CREATED})
            return Response({"msg":"Registration successful","status":status.HTTP_201_CREATED})
        # print(serializer.errors) it will work only if wedccx remove raise exception in line 14
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    # renderer_classes=[UserRenderer]
    def post(self, request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            print(user)
            if user:
                token=get_tokens_for_user(user) 
                return Response({"token":token,"msg":"login successful","user_role":user.roles,"status":status.HTTP_200_OK})
            else:
                #serializer use nahi kar rahe isliye custom handle karna pad raha hai..warna as above handle ho jata
                return Response({'errors':{'non_field_errors':["Email or password is not valid"]}},status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    # renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    # renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self, request,format=None):
        #we are passing the data which is not available in serializer,so for that we need to use the context argument.
        serializer=UserChangePasswordSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            return Response({"msg":"password changed successful","status":status.HTTP_200_OK})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetView(APIView):
    # renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"msg":"password reset link sent over the mail.Please check the Email Inbox","status":status.HTTP_200_OK})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    # renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={"uid":uid, "token":token})
        if serializer.is_valid():
            return Response({"msg":"password reset successfully","status":status.HTTP_200_OK})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetUserInfo(APIView):
    renderer_classes=[JSONRenderer]
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['airline_code','roles']
    search_fields = ['airline_code','roles']
    ordering_fields = ['id']

    def get(self, request,*args,**kwargs):
        # # todo:
        #     positive -> get specific user info if no user found then give err op
        #     negative -> get all user info
        #     else -> return error
        try:
            if kwargs:
                user_id = int(kwargs.get("key"))
                if user_id> 0:
                    user=get_object_or_404(User,id=user_id)
                    if user:
                        serializer = UserProfileSerializer(user)
                        return Response(serializer.data)
                else:
                    user=User.objects.all()
                    serializer = UserProfileSerializer(user, many=True)
                    return Response(serializer.data)
            else:
                return Response({'message': 'account not found', 'status': 400})
        except Exception:
            return Response({'message': 'invalid input ','status': 400})


class GetAllAirlineInfo(APIView):
    queryset=Mio_airline.objects.all()
    serializer_class=MioAirlineSerializer   


# class GetTerminalGateInfo(ListAPIView):
#     queryset=Mio_terminal.objects.all()
#     serializer_class=MioTerminalSerializer

# class GetFlightSchedule(ListAPIView):
#     queryset=Mio_flight_schedule.objects.all()
#     serializer_class=MioFlightScheduleSerializer


class Airline_create(APIView):
    serializer_class=MioAirlineSerializer
    
    def post(self, request,*args, **kwargs):
        try:
            airline_flight_key=request.data.get("airline_name")+request.data.get("airline_code") + "_" + request.data.get("flight_code")
            data=request.data
            data["airline_flight_key"]=airline_flight_key
            serializer=self.serializer_class(data=data)
            # NOTE
            # "dont worry about the payload validations,it will automatically takes only those fields which we mentioned in serializer....other than that it will ignore gracefully "
            if serializer.is_valid():
                serializer.save()
                return Response({"msg":"Airline data added successful","status":status.HTTP_200_OK})
            else:
                "to get this field is required error."
                return Response({"msg":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})
        except Exception:
            return Response({'message': 'invalid input ','status': 400})


class Airline_RUD(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,CreateModelMixin,GenericAPIView):
    queryset=Mio_airline.objects.all()
    serializer_class=MioAirlineSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class Terminal_create(APIView):
    serializer_class=MioTerminalSerializer

    def post(self, request,*args, **kwargs):
        try:
            serializer=self.serializer_class(data=request.data)
            # NOTE
            # "dont worry about the payload validations,it will automatically takes only those fields which we mentioned in serializer....other than that it will ignore gracefully "
            if serializer.is_valid():
                serializer.save()
                return Response({"msg":"Terminal data added successful","status":status.HTTP_200_OK})
            else:
                "to get this field is required error."
                return Response({"msg":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            return Response({"msg":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})



class Terminal_RUD(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):

    queryset=Mio_terminal.objects.all()
    serializer_class=MioTerminalSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FlightSchedule_create(APIView):
    serializer_class=MioFlightScheduleSerializer
    permission_classes=[IsAuthenticated,airline_employee_permission]

    def post(self, request,*args, **kwargs):
        req_user_airline=str(User.objects.get(email=request.user.email).airline_code)
        req_airline=request.data.get("airline_flight_key")[:3]
        if req_user_airline==req_airline:
            data=request.data
            dtm=datetime.datetime.strptime(data.get("time"),'%Y-%m-%d %H:%M:%S.%f')
            data["date"]=dtm.date()
            data["time"]=dtm.time()
            date_dtm=dtm.date().strftime("%Y_%m_%d")
            airline_flight_key=data.get('airline_flight_key')
            fact_guid=f"{airline_flight_key}_{date_dtm}"
            data["fact_guid"]=fact_guid
            serializer=self.serializer_class(data=data)
                # NOTEterminal_gate_key
            # "dont worry about the payload validations,it will automatically takes only those fields which we mentioned in serializer....other than that it will ignore gracefully "
            if serializer.is_valid():
                serializer.save()
                return Response({"msg":"Terminal data added successful","status":status.HTTP_200_OK})
            else:
                "to get this field is required error."
                return Response({"msg":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})
        else:
            return Response({"detail": "You do not have permission to perform this action.","status":status.HTTP_403_FORBIDDEN})





class FlightScehduleRUD(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset=Mio_flight_schedule.objects.all()
    serializer_class=MioFlightScheduleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AirlineInfo(ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    renderer_classes=[UserRenderer]
    permission_classes = (IsAuthenticated,airline_employee_permission)
    serializer_class = MioAirlineSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['airline_code','flight_code','airline_name','is_available']
    search_fields = ['airline_code','flight_code','airline_name','is_available']

    def get_queryset(self, *args, **kwargs):
        """
        TODO:
        We can do customization in the queryset we want 
        """
        user_airline_code=self.request.user.airline_code
        queryset_list=Mio_airline.objects.filter(airline_code=user_airline_code)
        return queryset_list



class AllTerminalGatesInfo(ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, adminpermission,)
    # queryset = Mio_terminal.objects.all()
    renderer_classes=[UserRenderer]
    serializer_class = MioTerminalSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gate_status','terminal_gate']
    search_fields = ['terminal_gate','gate_status']
    # ordering_fields = ['id']
    # pagination_class = MyPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        TODO:
        We can do customization in the queryset we want 
        """
        queryset_list=Mio_terminal.objects.all()
        return queryset_list


class FlightScehduleInfo(ListAPIView):
    
    # permission_classes = (IsAuthenticated)
    renderer_classes=[UserRenderer]
    serializer_class = MioFlightScheduleSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'time':['gte','lte'],'date':['gte','lte']}
    search_fields = ['airline_flight_key','source','destination','arrival_departure','date','time','terminal_gate_key','baggage_carousel','remarks']

    def get_queryset(self, *args, **kwargs):
        """
        TODO:
        We can do customization in the queryset we want 
        """
        queryset_list=Mio_flight_schedule.objects.all()
        return queryset_list

class PassengerInfo(ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, adminpermission,)
    # queryset = Mio_terminal.objects.all()
    serializer_class = MioPassengerSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['airline_flight_key','date','passenger_id']
    ordering_fields = ['date']
    # pagination_class = MyPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        TODO:
        We can do customization in the queryset we want 
        """
        queryset_list=Mio_passenger.objects.all()
        return queryset_list



class PassengerRUD(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset=Mio_passenger.objects.all()
    serializer_class=MioPassengerSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class Passenger_create(APIView):
    serializer_class=MioPassengerSerializer

    def post(self, request,*args, **kwargs):
    
        data=request.data
        
        date = data.get('flight_key')[-10:]
        data["airline_flight_key"] = data.get('flight_key')[:-11]

        date = datetime.datetime.strptime(date, "%Y_%m_%d")
        data["date"] = date.date().strftime("%Y-%m-%d")
        
        serializer=self.serializer_class(data=data)
            # NOTE
            # terminal_gate_key
        # "dont worry about the payload validations,it will automatically takes only those fields which we mentioned in serializer....other than that it will ignore gracefully "
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Flight passenger data added successful","status":status.HTTP_200_OK})
        else:
            "to get this field is required error."
            return Response({"msg":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})
    # except Exception as e:
    #         return Response({"msg":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})


class Baggagecreate(APIView):
    serializer_class=BaggageSerializer

    def post(self, request,*args, **kwargs):
        data=request.data        
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Baggage corosel data added successful","status":status.HTTP_200_OK})
        else:
            "to get this field is required error."
            return Response({"msg":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})
   

class BaggageRUD(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):

    queryset=BaggageCar.objects.all()
    serializer_class=BaggageSerializer
    permission_classes=[IsAuthenticated,airport_employee_permission]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class BaggageInfo(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, adminpermission,)
    # serializer_class = BaggageSerializer
    # filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['terminal_carousel',"hour_00","hour_01","hour_02","hour_03","hour_04","hour_05","hour_06","hour_07","hour_08","hour_09","hour_10","hour_11","hour_12","hour_13","hour_14","hour_15","hour_17","hour_18","hour_19","hour_20","hour_21","hour_22","hour_23"]
    # search_fields = ['terminal_carousel',"hour_00","hour_01","hour_02","hour_03","hour_04","hour_05","hour_06","hour_07","hour_08","hour_09","hour_10","hour_11","hour_12","hour_13","hour_14","hour_15","hour_17","hour_18","hour_19","hour_20","hour_21","hour_22","hour_23"]
    # ordering_fields =['terminal_carousel',"hour_00","hour_01","hour_02","hour_03","hour_04","hour_05","hour_06","hour_07","hour_08","hour_09","hour_10","hour_11","hour_12","hour_13","hour_14","hour_15","hour_17","hour_18","hour_19","hour_20","hour_21","hour_22","hour_23"]
    # # pagination_class = MyPageNumberPagination

    def get(self, request,format=None):
        hour=request.data['hour']
        queryset_list=BaggageCar.objects.values_list('terminal_carousel',hour)
        dt=[{i[0]:i[1] for i in queryset_list}]
        return Response({"data":dt,"status":status.HTTP_200_OK})


class GateMaintance(UpdateModelMixin,GenericAPIView):
    queryset=Mio_terminal.objects.all()
    serializer_class=MioTerminalSerializer
    permission_classes=[IsAuthenticated,airport_employee_permission]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

