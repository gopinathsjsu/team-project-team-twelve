from multiprocessing import context
from django.shortcuts import render
from jwtapp.models import Mio_airline, Mio_flight_schedule, Mio_terminal, User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from jwtapp.permissions import adminpermission
from jwtapp.serializers import MioAirlineSerializer, MioFlightScheduleSerializer, MioTerminalSerializer, UserRegistrationSerializer
from jwtapp.serializers import UserLoginSerializer
from jwtapp.renderers import UserRenderer
from rest_framework.generics import ListAPIView
# Create your views here.

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from jwtapp.serializers import UserProfileSerializer
from jwtapp.serializers import UserChangePasswordSerializer
from jwtapp.serializers import SendPasswordResetEmailSerializer
from jwtapp.serializers import UserPasswordResetSerializer
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


def get_fact_guid(source,destination,time):
    unique_sep="|"
    unique_ID = uuid.uuid5(uuid.NAMESPACE_X500,source + unique_sep + destination+unique_sep+time)
    return str(unique_ID)

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
        # print(serializer.errors) it will work only if we remove raise exception in line 14
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user:
                token=get_tokens_for_user(user) 
                return Response({"token":token,"msg":"login successful","status":status.HTTP_200_OK})
            else:
                #serializer use nahi kar rahe isliye custom handle karna pad raha hai..warna as above handle ho jata
                return Response({'errors':{'non_field_errors':["Email or password is not valid"]}},status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self, request,format=None):
        #we are passing the data which is not available in serializer,so for that we need to use the context argument.
        serializer=UserChangePasswordSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            return Response({"msg":"password changed successful","status":status.HTTP_200_OK})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"msg":"password reset link sent over the mail.Please check the Email Inbox","status":status.HTTP_200_OK})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializer(data=request.data,context={"uid":uid, "token":token})
        if serializer.is_valid():
            return Response({"msg":"password reset successfully","status":status.HTTP_200_OK})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GetUserInfo(APIView):
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


class GetTerminalGateInfo(ListAPIView):
    queryset=Mio_terminal.objects.all()
    serializer_class=MioTerminalSerializer

class GetFlightSchedule(ListAPIView):
    queryset=Mio_flight_schedule.objects.all()
    serializer_class=MioFlightScheduleSerializer


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



class AirlineInfo(ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, adminpermission,)
    # queryset = Mio_terminal.objects.all()
    serializer_class = MioAirlineSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['airline_code','flight_code','airline_name','is_available']
    search_fields = ['airline_code','flight_code','airline_name','is_available']
    # ordering_fields = ['id']
    # pagination_class = MyPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        TODO:
        We can do customization in the queryset we want 
        """
        queryset_list=Mio_airline.objects.all()
        return queryset_list



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


class AllTerminalGatesInfo(ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, adminpermission,)
    # queryset = Mio_terminal.objects.all()
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


class FlightSchedule_create(APIView):
    serializer_class=MioFlightScheduleSerializer

    def post(self, request,*args, **kwargs):
    
        data=request.data
        source=data.get('source')
        destination=data.get('destination')
        time=data.get('time')
        fact_guid=get_fact_guid(source,destination,time)
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
    # except Exception as e:
    #         return Response({"msg":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})

class FlightScehduleRUD(GenericAPIView):
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


class FlightScehduleInfo(ListAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, adminpermission,)
    # queryset = Mio_terminal.objects.all()
    serializer_class = MioFlightScheduleSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source','destination','arrival_departure','terminal_gate_key','baggage_carousel']
    search_fields = ['source','destination','arrival_departure','terminal_gate_key','baggage_carousel']
    ordering_fields = ['time']
    # pagination_class = MyPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        TODO:
        We can do customization in the queryset we want 
        """
        queryset_list=Mio_flight_schedule.objects.all()
        return queryset_list
