from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse

from .jwt_util import create_jwt_token, decode_jwt_token

User = get_user_model()


class LoginView(APIView):
    @authentication_classes([])
    @permission_classes([])
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            token = create_jwt_token(user)
            return Response({"token": token})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationView(APIView):
    @authentication_classes([])
    @permission_classes([])
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        idName = request.data.get("idName")
        phoneNumber = request.data.get("phoneNumber")
        profilePicUrl = request.data.get("profilePicUrl")

        try:
            user = User.objects.create_user(
                email=email, password=password, idName=idName, phoneNumber=phoneNumber, profilePicUrl=profilePicUrl
            )
            token = create_jwt_token(user)
            return Response({"token": token})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
class ProtectedResourceView(APIView):
    def get(self, request, *args, **kwargs):
        idName = request.user.idName

        # Access granted, continue processing the request
        return Response({"message": f"Access granted for user {idName}"})


@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get("token")

        if token:
            decoded_token = decode_jwt_token(token)

            if decoded_token:
                user_id = decoded_token["user_id"]
                user = User.objects.get(idName=user_id)

                # Refresh the token
                refreshed_token = create_jwt_token(user)
                return Response({"token": refreshed_token})

        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
