from django.shortcuts import render,get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework import permissions,status
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



