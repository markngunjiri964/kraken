from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from internship.models import InternshipCategory, CVSubmission, Payment
from .serializers import (
    UserRegistrationSerializer, 
    OTPVerificationSerializer, 
    UserLoginSerializer,
    InternshipCategorySerializer,
    CVSubmissionSerializer,
    PaymentSerializer
)

User = get_user_model()

# User Registration View
class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = user.generate_otp()  # Generate OTP
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}.',
                'noreply@internshipplatform.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'User registered successfully. Check your email for OTP verification.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# OTP Verification View
class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'OTP verified successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({'message': 'Login successful!', 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Internship Category List View
class InternshipCategoryListView(generics.ListAPIView):
    queryset = InternshipCategory.objects.all()
    serializer_class = InternshipCategorySerializer

# CV Submission View
class CVSubmissionView(APIView):
    def post(self, request):
        serializer = CVSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'CV submitted successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Payment View
class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Payment recorded successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
