from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from core.models import  Raffle, Prize, Ticket, PrizeRaffle
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
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] 

class RaffleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Raffle
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ['ticketNumber']



class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = '__all__'

class CustomRaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raffle
        fields = ['id', 'name']


class CustomTicketSerializer(serializers.ModelSerializer):
    raffle = CustomRaffleSerializer()
    class Meta:
        model = Ticket
        fields = '__all__' 
        
class PrizeRaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrizeRaffle
        fields = '__all__'  

class CustomPrizeRaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrizeRaffle
        fields = '__all__'
        depth = 2

class CustomPrizeSerializer(serializers.ModelSerializer):
    winner = CustomTicketSerializer(source='prizeraffle_set.winnerTicket', read_only=True)

    class Meta:
        model = Prize
        fields = ['id', 'name', 'description', 'image', 'winner']

class CustomRaffleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    prizes = serializers.SerializerMethodField()

    class Meta:
        model = Raffle
        fields = [
            'id', 'ticket_limit', 'name', 'public_name', 'description', 
            'image', 'ticket_price', 'raffle_date', 'user', 'prizes'
        ]

    def get_prizes(self, obj):
        prizeraffles = PrizeRaffle.objects.filter(raffle=obj)
        return [
            {
                "prize": CustomPrizeSerializer(prizeraffle.prize).data,
                "winner": TicketSerializer(prizeraffle.winnerTicket).data if prizeraffle.winnerTicket else None,
            }
            for prizeraffle in prizeraffles
        ]