from django.urls import path
from .views import SignUpView, CodeVerifyView, GetNewCodeView, UserChangeInfoView, UserPhotoStatusView, LoginView, \
    LogoutView, LoginRefreshView,ForgotPasswordView,ResetPasswordCodeView,ResetPasswordView

urlpatterns=[
    path('signup/',SignUpView.as_view()),
    path('code_verify/',CodeVerifyView.as_view()),
    path('get_new_code/',GetNewCodeView.as_view()),
    path('change-info/', UserChangeInfoView.as_view()),
    path('change-photo/',UserPhotoStatusView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('loginrefresh/',LoginRefreshView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-code/', ResetPasswordCodeView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),

]