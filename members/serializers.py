from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        field = ['email', 'password']

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        user_type = attrs.get('user_type')

        # validation for employers
        if user_type == 'employer':
            if not attrs.get('company_name'):
                raise ValidationError('Employers must have company name')
            if not attrs.get('company_website'):
                raise ValidationError('Company website is required for employers')

        # validation for job seekers
        if user_type == 'job_seeker':
            if not attrs.get('bio'):
                raise ValidationError('A short bio is important for job seekers')

            if not attrs.get('contact'):
                raise ValidationError('Contact info is required for job seekers')

        if email_exists:
            raise ValidationError('email already exist')
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'user_type']
