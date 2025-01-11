from django.contrib.auth import authenticate
from rest_framework import status
import logging
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .token import create_jwt_pair_for_users
from .serializers import SignUpSerializer, UserSerializer
from .models import User
from rest_framework import generics, permissions
from django.http import JsonResponse
from django.db import connection

logger = logging.getLogger(__name__)


def test_db_connection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")  # Simple query to check connection
            result = cursor.fetchone()
        return JsonResponse({"status": "success", "result": result})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


class LoginView(APIView):
    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_users(user)
            user_data = UserSerializer(user).data
            response = {
                'message': 'Login successful',
                'tokens': tokens,
                'user': user_data

            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'invalid username or password'}, status=status.HTTP_200_OK)

    def get(self, request: Request):
        content = {
            'user': str(request.user),
            'auth': str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                response = {
                    'message': 'User created successfully',
                    'data': serializer.data
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            logger.error(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"SignUp failed: {str(e)}", exc_info=True)
            return Response(
                data={'error': 'An unexpected error occurred. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Create your views here.
