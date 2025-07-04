from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ExpenseIncome
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from decimal import Decimal

User = get_user_model() 
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        Check that the two passwords match.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Delete password2 prior to user creation since the User model will not take it.
        validated_data.pop('password2')

        # Remember to use createuser or createsuperuser so that the password is hashed properly.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''), 
            password=validated_data['password']
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['username', 'email']

class ExpenseIncomeSerializer(serializers.ModelSerializer):
    # Bind model's 'total_amount' with API response's 'total'.
    total = serializers.DecimalField(source='total_amount', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ExpenseIncome
        fields = [
            'id', 'title', 'description', 'amount',
            'transaction_type', 'tax', 'tax_type', 'date',
            'total', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total']


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if user.is_superuser and validated_data.get('user') is not None:
            transaction_user = validated_data['user']
            if not User.objects.filter(pk=transaction_user.pk).exists():
                 raise serializers.ValidationError({"user": "Specified user does not exist."})
        else:
            transaction_user = user

        validated_data['user'] = transaction_user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        # Handle user assignment for superusers
        if user.is_superuser and validated_data.get('user') is not None:
            if not User.objects.filter(pk=validated_data['user'].pk).exists():
                 raise serializers.ValidationError({"user": "Specified user does not exist."})
            instance.user = validated_data.get('user', instance.user)
        # Regular users cannot change the user of a record
        elif 'user' in validated_data and validated_data['user'].pk != user.pk:
            raise serializers.ValidationError({"user": "You cannot change the user of a record."})

        return super().update(instance, validated_data)

    def validate(self, data):
        request = self.context.get('request')

        if 'tax_amount_calculated' in data:
            raise serializers.ValidationError({"tax_amount_calculated": "This field is calculated automatically and cannot be set directly."})
        if 'total_amount' in data: 
            raise serializers.ValidationError({"total_amount": "This field is calculated automatically and cannot be set directly."})
        if 'total' in data: 
            raise serializers.ValidationError({"total": "This field is calculated automatically and cannot be set directly."})

        if request.method in ['PUT', 'PATCH'] and not request.user.is_superuser:
            if 'user' in data and data['user'] != request.user:
                raise serializers.ValidationError(
                    {"user": "Regular users can only update their own records and cannot change the assigned user."}
                )
            if self.instance and self.instance.user != request.user:
                 raise serializers.ValidationError(
                    {"detail": "You do not have permission to update this record."}
                )

        return data

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive value.")
        return value

    def validate_transaction_type(self, value):
        if value not in ['credit', 'debit']:
            raise serializers.ValidationError("Transaction type must be 'credit' or 'debit'.")
        return value

    def validate_tax_type(self, value):
        if value not in ['flat', 'percentage']:
            raise serializers.ValidationError("Tax type must be 'flat' or 'percentage'.")
        return value


class ExpenseIncomeListSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(source='total_amount', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ExpenseIncome
        fields = [
            'id', 'title', 'amount', 'transaction_type', 'total', 'created_at'
        ]
        read_only_fields = ['id', 'title', 'amount', 'transaction_type', 'total', 'created_at']