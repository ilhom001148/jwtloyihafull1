from django.urls import path
from .views import SignUpView, CodeVerifyView, GetNewCodeView, UserChangeInfoView, UserPhotoStatusView, LoginView, \
    LogoutView, LoginRefreshView,ForgotPasswordView,ResetPasswordCodeView,ResetPasswordView,CommentCreateView,CommentUpdateView, \
    CommentListView,CommentDeleteView,PostCreateView,PostListView,PostDetailView,PostDeleteView,PostUpdateView

# from .views import *

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

    path('post-create/',PostCreateView.as_view()),
    path('list-post/',PostListView.as_view()),
    path('post-update/<int:pk>/',PostUpdateView.as_view()),
    path('post-delete/<int:pk>/',PostDeleteView.as_view()),
    path('post-detail/<int:pk>/', PostDetailView.as_view()),

    path('comment-create/',CommentCreateView.as_view()),
    path('comment-update/',CommentUpdateView.as_view()),
    path('comment-list/',CommentListView.as_view()),
    path('comment-delete/',CommentDeleteView.as_view()),


]