from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser, VIA_EMAIL, VIA_PHONE
from shared.utility import check_email_or_phone
from rest_framework import status
from django.db.models import Q


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    auth_status = serializers.CharField(read_only=True)
    auth_type = serializers.CharField(read_only=True)

    email_or_phone = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'auth_status', 'auth_type', 'email_or_phone']

    def validate(self, attrs):
        user_input = attrs.pop('email_or_phone')
        user_data = self.auth_validate(user_input)
        attrs.update(user_data)
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    @staticmethod
    def auth_validate(user_input):
        user_input_type = check_email_or_phone(user_input)

        if user_input_type == 'phone':
            return {
                'auth_type': VIA_PHONE,
                'phone': user_input
            }
        elif user_input_type == 'email':
            return {
                'auth_type': VIA_EMAIL,
                'email': user_input
            }
        else:
            raise ValidationError("Email yoki Telefon nomeringiz noto‘g‘ri kiritilgan")


    def validate_email_or_phone(self,email_or_phone):
        user=CustomUser.objects.filter( Q(phone=email_or_phone) | Q(email=email_or_phone)).exists()
        if user:
            raise ValidationError(detail="Bu telefon raqam yoki email bilan oldin ro'yxatdan o'tilgan")
        return email_or_phone















