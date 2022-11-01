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

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from jwtapp.serializers import UserProfileSerializer
from jwtapp.serializers import UserChangePasswordSerializer
from jwtapp.serializers import SendPasswordResetEmailSerializer
from jwtapp.serializers import UserPasswordResetSerializer
from django.shortcuts import get_object_or_404



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
            return Response({"token":token,"msg":"Registration successful","status":status.HTTP_201_CREATED})
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



class UserListView(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated, adminpermission,)
    
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    # pagination_class = MyPageNumberPagination
    # filter_backends = [DjangoFilterBackend,
                    #    filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['roles', 'org_id']
    # search_fields = ['email', 'first_name']
    # ordering_fields = ['pk']

    # def get_queryset(self, *args, **kwargs):
    #     print("in get query method")
        # org_id = User.objects.get(email=self.request.user).org_id
        # queryset_list = User.objects.filter(
        #     org_id=org_id).order_by('-id')

        # elif role == 'user':
        #     queryset_list = Project.objects.filter(
        #         created_by=self.request.user).order_by('-id')

        # return queryset_list


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




class GetAllAirlineInfo(ListAPIView):
    queryset=Mio_airline.objects.all()
    serializer_class=MioAirlineSerializer

class GetTerminalGateInfo(ListAPIView):
    queryset=Mio_terminal.objects.all()
    serializer_class=MioTerminalSerializer

class GetFlightSchedule(ListAPIView):
    queryset=Mio_flight_schedule.objects.all()
    serializer_class=MioFlightScheduleSerializer

