from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from jwtapp.models import User


class adminpermission(BasePermission):
    def has_permission(self, request, view):
        email = request.user.email
        user_roles = User.objects.get(email=email).roles
        if user_roles == 'admin':
            return True
        else:
            return False


# class userpermissions(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         user_roles = User.objects.get(email=email).roles
#         if user_roles == 'user':
#             return True
#         else:
#             return False


# class Allpermissions(BasePermission):
#     def has_permission(self, request, view):
#         user = request.user
#         user_roles = User.objects.get(email=email).roles
#         if user_roles == 'user' or user_roles == 'admin':
#             return True
#         else:
#             return False