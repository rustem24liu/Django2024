from email.policy import default
from os import write

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import Group

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    role = serializers.ChoiceField(choices=['Student', 'Teacher', 'Admin' ], default='Student', write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'Error': 'Password does not match'})

        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'Error': 'Email is already used'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        role = self.validated_data['role']
        group = Group.objects.get(name=role)
        account.groups.add(group)

        return account

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False)  # Optional field for role update

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']

    def update(self, instance, validated_data):
        role = validated_data.get('role', None)
        if role:
            if not self.context['request'].user.is_superuser:
                raise serializers.ValidationError("Only Admin can change roles.")

            group = Group.objects.get(name=role)
            instance.groups.clear()
            instance.groups.add(group)

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance