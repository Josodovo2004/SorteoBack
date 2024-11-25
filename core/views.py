from rest_framework.response import Response
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer, LoginSerializer, PrizeRaffleSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from core.models import Raffle, Ticket, Prize, PrizeRaffle
from .filters import UserFilter, TicketFilter, RaffleFilter, PrizeFilter, PrizeRaffleFilter
from .serializers import (UserSerializer, LoginSerializer, 
                          RegisterSerializer, RaffleSerializer, 
                          PrizeSerializer, TicketSerializer, 
                          CustomTicketSerializer, CustomPrizeRaffleSerializer)
from django_filters.rest_framework import DjangoFilterBackend
import random
from rest_framework.permissions import IsAuthenticated, AllowAny


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_summary="User registration",
        operation_description="Registers a new user with the provided data.",
        responses={201: openapi.Response("Created", schema=RegisterSerializer)}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "User created successfully",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="User login",
        operation_description="Authenticates a user and returns an access token on successful login.",
        request_body=LoginSerializer,
        responses={200: openapi.Response("Success", schema=LoginSerializer)}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        serialized_user = UserSerializer(user).data

        response = Response({
            'access': access,
            'user_id': serialized_user['id'],
            'username': serialized_user['username'],
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax',
            max_age=60 * 60 * 24 * 7
        )

        return response


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data['custom_message'] = 'Welcome!'
        refresh_token = response.data['refresh']
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            samesite='Lax',
            max_age=60 * 60 * 24 * 7
        )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token not found.'}, status=401)
        data = {'refresh': refresh_token}
        request.data['refresh'] = refresh_token
        return super().post(request, *args, **kwargs)


class RaffleListView(generics.ListCreateAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RaffleFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  
        return [AllowAny()]


class RaffleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer


class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketSerializer  
        return CustomTicketSerializer 
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  
        return [AllowAny()] 


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class PrizeListView(generics.ListCreateAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrizeFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  
        return [AllowAny()]


class PrizeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer


class PrizeRaffleCreateView(generics.CreateAPIView):
    queryset = PrizeRaffle.objects.all()
    serializer_class = PrizeRaffleSerializer

class PrizeRaffleListView(generics.ListAPIView):
    queryset = PrizeRaffle.objects.all()
    serializer_class = CustomPrizeRaffleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrizeRaffleFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  
        return [AllowAny()]

class PrizeRaffleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PrizeRaffle.objects.all()
    serializer_class = PrizeRaffleSerializer


class RaffleView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the winner of a specified Raffle.",
        manual_parameters=[
            openapi.Parameter(
                'raffle_id',
                openapi.IN_QUERY,
                description="ID of the Raffle.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Winner ticket details.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'winner': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Details of the winning ticket.",
                        ),
                    },
                ),
            ),
            400: "Bad Request: Missing or invalid parameters.",
            404: "Not Found: Raffle or tickets not found.",
        },
    )
    def get(self, request):
        raffle_id = request.query_params.get('raffle_id')
        if not raffle_id:
            return Response(
                {"error": "The 'raffle_id' parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            raffle_id = int(raffle_id)
        except ValueError:
            return Response(
                {"error": "The 'raffle_id' parameter must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        raffle = Raffle.objects.filter(id=raffle_id).first()
        if not raffle:
            return Response(
                {"error": f"Raffle with id {raffle_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        tickets = list(Ticket.objects.filter(raffle=raffle))
        if not tickets:
            return Response(
                {"error": f"No tickets found for Raffle with id {raffle_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        random.shuffle(tickets)
        winner_index = random.randint(0, len(tickets) - 1)
        winner = tickets[winner_index]
        winner.is_winner = True
        winner.save()

        winner_ticket = CustomTicketSerializer(winner).data
        return Response({'winner': winner_ticket}, status=status.HTTP_200_OK)


class GetPaidTickets(APIView):

    @swagger_auto_schema(
        operation_summary="Get Paid Tickets",
        operation_description="Returns the count of paid tickets (`status=True`) for a given Raffle identified by `raffle_id`.",
        manual_parameters=[
            openapi.Parameter(
                name="raffle_id",
                in_=openapi.IN_QUERY,
                description="The ID of the Raffle to retrieve paid tickets for.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful response with the count of paid tickets.",
                examples={"application/json": {"paid_tickets": 5}},
            ),
            400: openapi.Response(
                description="Bad Request - Missing or invalid `raffle_id`.",
                examples={"application/json": {"error": "The 'raffle_id' parameter must be an integer."}},
            ),
            404: openapi.Response(
                description="Not Found - Raffle or tickets not found.",
                examples={"application/json": {"error": "Raffle with id 123 not found."}},
            ),
        },
    )
    def get(self, request):
        raffle_id = request.query_params.get('raffle_id')
        if not raffle_id:
            return Response(
                {"error": "The 'raffle_id' parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            raffle_id = int(raffle_id)
        except ValueError:
            return Response(
                {"error": "The 'raffle_id' parameter must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        raffle = Raffle.objects.filter(id=raffle_id).first()
        if not raffle:
            return Response(
                {"error": f"Raffle with id {raffle_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        paid_tickets_count = Ticket.objects.filter(raffle=raffle, status=True).count()

        return Response({"paid_tickets": paid_tickets_count}, status=status.HTTP_200_OK)
