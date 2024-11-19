from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from core.models import  Sorteo, Premio, Ticket, PremioSorteo
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        celular = validated_data.pop('celular', None)

        # Create user instance
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user  # Return the created user instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(_('Invalid credentials'))

        attrs['user'] = user  # Store the user instance in validated data

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)

        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  # Include other fields as needed

class SorteoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()

    class Meta:
        model = Sorteo
        fields = ['id', 'limiteTickets', 'usuario']


class TicketSerializer(serializers.ModelSerializer):
    sorteo = SorteoSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'


class PremioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premio
        fields = '__all__'


class CustomTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__' 
        depth = 2  
        
class PremioSorteoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PremioSorteo
        fields = '__all__'  # Includes all fields in the model