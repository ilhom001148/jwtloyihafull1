from http.client import responses

from django.shortcuts import render,get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework import permissions,status
from rest_framework.permissions import IsAuthenticated

from .serializers import SignUpSerializer,UserChangeInfoSerializer,UserPhotoStatusSerializer,LoginSerializer
from .models import CustomUser,NEW,CODE_VERIFY,DONE,PHOTO_DONE,VIA_EMAIL,VIA_PHONE
from rest_framework.views import APIView
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils import timezone
from .models import CodeVerify,CustomUser
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken




class SignUpView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer
    queryset = CustomUser




class CodeVerifyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        user=request.user
        code=self.request.data.get('code')

        codes = CodeVerify.objects.filter(user=user,code=code,expiration_time__gte=timezone.now()).first()
        # codes=user.verify_codes.filter(code=code,expiration_time__gte=datetime.now(),is_active=False)
        if not codes:
            raise ValidationError({'message':'Kodingiz xato yoki eskirgan','status':status.HTTP_400_BAD_REQUEST})
        else:
            codes.is_active=True
            codes.save()
        if user.auth_status==NEW:
            user.auth_status=CODE_VERIFY
            user.save()
        response_data={
            'message':'Kod tasdiqlandi',
            'status':status.HTTP_200_OK,
            'access':user.token()['access'],
            'refresh':user.token()['refresh']
        }
        return Response(response_data)

class GetNewCodeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        user=request.user
        codes = User.Verify_codes.filter(expiration_time__gte=datetime.now(),is_active=False)
        if code.exists():
            raise ValidationError({'message':'Sizda holi active code bor','status':status.HTTP_400_BAD_REQUEST})
        else:
            if user.auth_type == VIA_EMAIL:
                code = user.generate_code(VIA_EMAIL)
                print(code, '1111111111111111111111111111111')
            elif user.auth_type == VIA_PHONE:
                code = user.generate_code(VIA_PHONE)
                print(code, '11111111111111111111111111111111111')

        response_data = {
            'message': 'Kod yuborildi',
            'status': status.HTTP_201_CREATED,
        }
        return Response(response_data)

#
# class UserChangeInfoView(APIView):
#     def get_object(self,pk):
#         user=get_object_or_404(CustomUser,pk=pk)
#         return user
#
#     def put(self,request,pk):
#         user=self.get_object(pk)
#         serializer=UserChangeInfoSerializer(instance=user,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             token,created=Token.objects.get_or_create(user=user)
#             return Response({
#                 "status":status.HTTP_200_OK,
#                 "message":"Ma'lumotlar muvaffaqiyatli yangilandi",
#                 "auth_status":user.auth_status,
#                 "token":token.key
#             })
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserChangeInfoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def put(self,request):
        user=request.user
        serializer=UserChangeInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user, validated_data=serializer.validated_data)

        response={
            'message':'malumotingiz qoshildi',
            'status':status.HTTP_200_OK,
            'access':user.token()['access'],
            'refresh':user.token()['refresh'],
        }
        return Response(response)




class UserPhotoStatusView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def patch(self,request):
        user=request.user
        serializer=UserChangeInfoSerializer(data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user, validated_data=serializer.validated_data)

        response={
            'message':'Rasm qoshildi',
            'status':status.HTTP_200_OK,
            'access':user.token()['access'],
            'refresh':user.token()['refresh'],
        }
        return Response(response)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer



class LogoutView(APIView):
    def post(self,request):
        try:
            refresh_token=RefreshToken(refresh)
            refresh_token.blacklist()
        except Exception as e:
            raise ValidationError(detail='xatolik: {e)')

        else:
            response_data={
                'status':status.HTTP_200_OK,
                'message':'tizimdan chiqdingiz'
            }
            return Response(response_data)



class LoginRefreshView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,request):
        refresh=self.request.data.get('refresh',None)
        try:
            refresh_token=RefreshToken(refresh)
        except Exception as e:
            raise ValidationError(detail=f'Xatolik: {e}')

        else:
            response_data={
                'status':status.HTTP_201_CREATED,
                'access':str(refresh_token.access_token)
            }
            return Response(response_data)



class ForgotPasswordView(APIView):
    permission_classes = (AllowAny, )
    def post(self,request):
        serializer=ForgotPasswordSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.validated_data
        response = {
            'status': status.HTTP_200_OK,
            "message": response_data.get('message'),
            "access": response_data.get('access'),
            "refresh": response_data.get('refresh'),
        }
        return Response(response)


class ResetPasswordCodeView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self,request):
        code=self.request.data.get('code')
        user=self.request.user
        user_code = CodeVerify.objects.filter(code=code, user=user,
                                              expiration_time__gte=datetime.now(), is_active=True
                                              )
        if not user_code.exists():
            raise ValidationError({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "Kodingiz xato yoki eskirgan"
            })
        else:
            user_code.update(is_active=False)


        response = {
            'status': status.HTTP_200_OK,
            'message': 'Kodingiz tasdiqlandi',
        }
        return Response(response)



class ResetPasswordView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self,request):
        user=request.user
        serializer=ResetPasswordSerializers(data=request.data,instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response={
            'status':status.HTTP_200_OK,
            'message':"Siz muffaqiyatli parolizni tikladiz",
        }
        return Response(response)








