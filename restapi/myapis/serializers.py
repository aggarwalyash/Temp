from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    CharField,EmailField,HyperlinkedIdentityField,ModelSerializer,SerializerMethodField,ValidationError
    )
from .models import *
User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username','email','first_name','last_name',
        ]

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            'username','email','email2','password',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return data


    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                username = username,
                email = email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        email = data['email']
        username = data['username']
        user_email = User.objects.filter(email=email)
        user_username = User.objects.filter(username=username)
        if user_email.exists() and user_username.exists():
            return data
        raise ValidationError("User does not exist")

class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email')


class ProfileCreateUpdateSerializer(ModelSerializer):
    user = UserLoginSerializer()
    class Meta:
        model = Profile
        fields = ['user','gender','address']

    def create(self, validated_data):
        user = validated_data['user']
        gender = validated_data['gender']
        address = validated_data['address']
        prof_obj = Profile(
                gender = gender,
                address = address
            )
        prof_obj.user = user
        prof_obj.save()
        return validated_data
