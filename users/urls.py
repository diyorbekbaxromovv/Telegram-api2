from django.urls import path
from .views import SignUpView, VerifyView, ResendVerifyView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyView.as_view()),
    path('resend_verify/', ResendVerifyView.as_view()),
]
