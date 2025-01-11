from django.urls import path
from .views import SignUpView, LoginView,test_db_connection

urlpatterns = [
    path('register', SignUpView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('test-db', test_db_connection),


]
