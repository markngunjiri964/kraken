from django.urls import path
from .views import RegisterUserView, VerifyOTPView, InternshipCategoryListView, CVSubmissionView, PaymentView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('internship-categories/', InternshipCategoryListView.as_view(), name='internship-categories'),
    path('cv-submission/', CVSubmissionView.as_view(), name='cv-submission'),
    path('payments/', PaymentView.as_view(), name='payments'),
    ]
