from multiprocessing import context
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from jwtapp.serializers import UserRegistrationSerializer
from jwtapp.serializers import UserLoginSerializer
from jwtapp.renderers import UserRenderer
# Create your views here.

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from jwtapp.serializers import UserProfileSerializer
from jwtapp.serializers import UserChangePasswordSerializer
from jwtapp.serializers import SendPasswordResetEmailSerializer
from jwtapp.serializers import UserPasswordResetSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
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

