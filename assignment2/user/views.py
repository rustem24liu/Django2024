from django.utils import timezone

from django.contrib.auth.models import Group, Permission

from os import access

from django.core.serializers import serialize
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from tutorial.quickstart.serializers import UserSerializer
from .serializers import UserRegisterSerializer, UserProfileUpdateSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from students.models import Student



# Create your views here.

# def create_default_groups():
#     roles = ["Student", "Teacher", "Admin"]
#     for role in roles:
#         Group.objects.get_or_create(name=role)

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def about_user(request):
    user = request.user
    roles = [group.name for group in user.groups.all()]
    return Response({
        'id': user.id,
        'username':user.username,
        'email':user.email,
        'first_name':user.first_name,
        'last_name':user.last_name,
        'is_staff':user.is_staff,
        'role':roles
    })

@api_view(['POST', ])
@permission_classes([IsAdminUser])
def register_view(request):
    # create_default_groups()
    # if request.user.is_authenticated:

    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            token, created = Token.objects.get_or_create(user=account)

            role = request.data.get('role', 'Student')
            group = Group.objects.get(name=role)
            account.groups.add(group)

            if role == 'Student':
                Student.objects.create(user=account,
                                        name=account.username,
                                       dob=request.data.get('dob'),
                                       email=account.email,
                                       registration_date=timezone.now()
                                       )
            if role == 'Admin':
                all_permissions = Permission.objects.all()
                group.permissions.set(all_permissions)
                print(all_permissions)
                account.user_permissions.set(all_permissions)
                account.save()

            data['response'] = 'Account has been created'
            data['username'] = account.username
            data['email'] = account.email
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)
        # else:
        #     print('you are logged in')

class Authentication(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)


class UserProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"})
        else:
            return Response(serializer.errors, status=400)