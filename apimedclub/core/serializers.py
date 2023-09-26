from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ('url', 'full_name')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'},

    )

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('url', 'profile', 'username', 'email', 'password')

    def create(self, validated_data):
        profile_data = validated_data['profile']
        password = make_password(validated_data['password'])

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password
        )

        profile = Profile.objects.create(
            user=user,
            full_name=profile_data['full_name'],
        )

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data['profile']

        if 'password' in validated_data:
            password = make_password(validated_data['password'])
            instance.password = password

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        profile = instance.profile
        profile.full_name = profile_data.get('full_name', profile.full_name)
        profile.save()

        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        for attr, value in validated_data.items():
            print("{}={}".format(attr, value))
            setattr(instance, attr, value)

        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])

        instance.save()
        return instance