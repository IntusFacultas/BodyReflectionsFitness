from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    is_staff = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_date_joined(self, obj):
        return obj.date_joined.strftime("%Y-%m-%dT%H:%M:%S")

    def get_is_staff(self, obj):
        return obj.user.is_staff

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "age",
            "gender",
            "date_joined",
            "email",
            "is_staff",
            "username"
        ]
