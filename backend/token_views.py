from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.middleware import csrf
from django.conf import settings
from django.contrib.auth import authenticate


class LoginApiView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            if user.is_active:
                response = Response(serializer.validated_data, status=status.HTTP_200_OK)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=serializer.validated_data['access'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY']
                )
                response.set_cookie(
                    key='refresh_token',
                    value=serializer.validated_data['refresh'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY']
                )
                csrf.get_token(request)
            else:
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
        return response


class RefreshApi(TokenRefreshView):
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=
                                         {'refresh': request.COOKIES.get("refresh_token")}
                                         )
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=serializer.validated_data['access'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY']
        )
        return response
