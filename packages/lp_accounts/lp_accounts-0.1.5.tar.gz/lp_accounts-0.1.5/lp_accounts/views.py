from django.conf import settings
from django.core import mail
from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UserSerializer, PasswordResetSerializer, PasswordUpdateSerializer, AuthTokenSerializer
from .models import User
from rest_condition import Or
from .permissions import IsAnonUser


class AccountCreate(generics.CreateAPIView):
    """
    post: Create new user
    """
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        Or(IsAnonUser, permissions.IsAdminUser)
    ]

    def post(self, request):
        response = super(AccountCreate, self).post(request)
        token, created = Token.objects.get_or_create(user_id=response.data['id'])
        return Response({'token': token.key, 'id': token.user_id}, status=status.HTTP_201_CREATED)


class AccountDetails(generics.RetrieveAPIView):
    """
    get: Retrieve user details
    """
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user


class PasswordReset(generics.GenericAPIView):
    """
    post: Send password reset email
    """
    serializer_class = PasswordResetSerializer
    permission_classes = {
        IsAnonUser
    }

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token, created = Token.objects.get_or_create(user=serializer.user)
        mail.send_mail(
            settings.RESET_PASSWORD_SUBJECT, 'This is the link: ' + token.key,
            settings.RESET_PASSWORD_SENDER, [request.data['email']],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordUpdate(generics.GenericAPIView):
    """
    post: Update user password
    """
    model = User
    serializer_class = PasswordUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [
        IsAnonUser
    ]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(request.data['password'])
        serializer.user.save()

        return Response(status=status.HTTP_200_OK)


class ObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    permission_classes = [
        IsAnonUser
    ]
