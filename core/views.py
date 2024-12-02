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
                          CustomTicketSerializer, CustomPrizeRaffleSerializer,
                          CustomRaffleSerializer)
from django_filters.rest_framework import DjangoFilterBackend
import random
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime


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
    queryset = Raffle.objects.all().order_by('-raffle_date')
    serializer_class = RaffleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RaffleFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]      
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RaffleSerializer  
        return CustomRaffleSerializer 


class RaffleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]      
    #     return [IsAuthenticated()]


class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketSerializer  
        return CustomTicketSerializer 


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]      
        return [IsAuthenticated()]


class PrizeListView(generics.ListCreateAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrizeFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]      
        return [IsAuthenticated()]


class PrizeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]      
        return [IsAuthenticated()]


class PrizeRaffleCreateView(generics.CreateAPIView):
    queryset = PrizeRaffle.objects.all()
    serializer_class = PrizeRaffleSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]      
        return [IsAuthenticated()]

class PrizeRaffleListView(generics.ListAPIView):
    queryset = PrizeRaffle.objects.all()
    serializer_class = CustomPrizeRaffleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrizeRaffleFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]      
        return [IsAuthenticated()]

class PrizeRaffleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PrizeRaffle.objects.all()
    serializer_class = PrizeRaffleSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]      
        return [IsAuthenticated()]


class RaffleView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the winner of a specified Raffle and Prize.",
        manual_parameters=[
            openapi.Parameter(
                'raffle_id',
                openapi.IN_QUERY,
                description="ID of the Raffle.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                'prize_id',
                openapi.IN_QUERY,
                description="ID of the Prize within the specified Raffle.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Winner ticket details for the specified prize.",
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
            404: "Not Found: Raffle, prize, or tickets not found.",
        },
    )
    def get(self, request):
        raffle_id = request.query_params.get('raffle_id')
        prize_id = request.query_params.get('prize_id')

        if not raffle_id or not prize_id:
            return Response(
                {"error": "Both 'raffle_id' and 'prize_id' parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            raffle_id = int(raffle_id)
            prize_id = int(prize_id)
        except ValueError:
            return Response(
                {"error": "'raffle_id' and 'prize_id' must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        raffle = Raffle.objects.filter(id=raffle_id).first()
        if not raffle:
            return Response(
                {"error": f"Raffle with id {raffle_id} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        prize = Prize.objects.filter(id=prize_id).first()  

        prizeRaffle = PrizeRaffle.objects.filter(raffle__id=raffle.id, prize__id=prize.id).first()
        if not prizeRaffle:
            return Response(
                {"error": f"Prize with id {prize_id} not found in Raffle {raffle_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        tickets = list(Ticket.objects.filter(raffle=raffle, is_paid=True,is_active=True))  
        if not tickets:
            return Response(
                {"error": f"No tickets found for Raffle {raffle_id}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        random.shuffle(tickets)
        winner_index = random.randint(0, len(tickets) - 1)
        winner = tickets[winner_index]
        prizeRaffle.winnerTicket =winner
        prizeRaffle.save()
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

        paid_tickets_count = Ticket.objects.filter(raffle=raffle, is_paid=True).count()

        return Response({"paid_tickets": paid_tickets_count}, status=status.HTTP_200_OK)


class WinnersListApiView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the winners of a specific Raffle. The tickets must have the is_paid and is_active field set to True in orde to be taken in consideration",
        manual_parameters=[
            openapi.Parameter(
                'raffle_id',
                openapi.IN_QUERY,
                description="ID of the Raffle for which to retrieve the winners.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="List of winners with their prizes.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="PrizeRaffle ID."),
                            "prize": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Prize ID."),
                                    "name": openapi.Schema(type=openapi.TYPE_STRING, description="Prize name."),
                                    "description": openapi.Schema(type=openapi.TYPE_STRING, description="Prize description."),
                                    "image": openapi.Schema(type=openapi.TYPE_STRING, description="Prize image URL."),
                                },
                                description="Details of the prize.",
                            ),
                            "winnerTicket": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Winning ticket ID."),
                                    "buyer_name": openapi.Schema(type=openapi.TYPE_STRING, description="Buyer's name."),
                                    "email": openapi.Schema(type=openapi.TYPE_STRING, description="Buyer's email."),
                                    "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description="Buyer's phone number."),
                                    "total_paid": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="Total amount paid for the ticket."),
                                    "is_winner": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether the ticket is a winner."),
                                },
                                description="Details of the winning ticket.",
                            ),
                        },
                    ),
                ),
            ),
            400: "Bad Request: Missing or invalid 'raffle_id'.",
            404: "Not Found: Raffle or winners not found.",
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
        
        prizes = PrizeRaffle.objects.filter(raffle__id=raffle.id)
        winners = []

        for prize in prizes:
            if prize.winnerTicket:
                winners.append(prize)
        
        serializedWinners = CustomPrizeRaffleSerializer(winners, many=True).data

        return Response(serializedWinners, status=status.HTTP_200_OK)
    

class SetTicketsPaidView(APIView):
    permission_classes = [IsAuthenticated]

    
    def post(self, request):
        ticket_ids = request.data.get('tickets', [])
        raffle_id = request.data.get('raffle_id')

        
        if not isinstance(ticket_ids, list):
            return Response({"error": "Invalid input, 'tickets' should be a list of ticket IDs."}, status=status.HTTP_400_BAD_REQUEST)

        if not raffle_id:
            return Response({"error": "Raffle ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        
        updated_tickets = Ticket.objects.filter(id__in=ticket_ids, raffle__id=int(raffle_id)) \
            .update(is_paid=True, is_active=True)

        
        tickets = Ticket.objects.filter(id__in=ticket_ids, raffle__id=int(raffle_id))

        
        serialized_tickets = TicketSerializer(tickets, many=True).data

        return Response({"tickets": serialized_tickets}, status=status.HTTP_200_OK)
    
class CreateManyTickets(APIView):
    
    def post(self, request):
        client_data = request.data.get('client_data') 
        raffle_id = request.data.get('raffle_id')
        quantity = int(request.data.get('quantity'))

        if not client_data:
            return Response({'error': 'Debe enviarse el client_data'}, status=status.HTTP_400_BAD_REQUEST)
        if not raffle_id:
            return Response({'error': 'Debe enviarse el raffle_id'}, status=status.HTTP_400_BAD_REQUEST)
        if not quantity:
            return Response({'error': 'Debe enviarse el valor quantity'}, status=status.HTTP_400_BAD_REQUEST)
        tickets = []
        for i in range(quantity):
            try:
                newTicket = Ticket()
                newTicket.buyer_name = client_data['name']
                newTicket.phone_number = client_data['phone_number']
                newTicket.email = client_data['email']
                newTicket.sale_date = str(datetime.now())
                newTicket.raffle = Raffle.objects.filter(id = raffle_id).first()
                newTicket.save()
                tickets.append(newTicket)
            except Exception as e:
                return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response = client_data
        ticketResponse = []
        for value in tickets:
            value : Ticket
            ticketResponse.append({
                'id' : value.id,
                'is_active' : value.is_active,
                'is_paid': value.is_paid,
                'sale_date' : value.sale_date,
                'total_paid' : value.total_paid,
                'raffle' : value.raffle.id,
                'ticket_number' : value.ticketNumber
            })
        response['tickets'] = ticketResponse

        return Response(response, status=status.HTTP_201_CREATED)

class TicketBuyersView(APIView):
    def get(self, request, raffle_id):
        try:
            # Filter tickets by raffle
            tickets = Ticket.objects.filter(raffle_id=raffle_id)
            raffle = Raffle.objects.filter(id=raffle_id).first()

            response = RaffleSerializer(raffle).data

            if not tickets.exists():
                return Response({"detail": "No tickets found for the given raffle."}, status=status.HTTP_404_NOT_FOUND)

            # Group buyers by DNI or phone number
            buyers = {}
            for ticket in tickets:
                # Use DNI as the key if available; otherwise, use phone number
                key = ticket.dni if ticket.dni else ticket.phone_number
                if key:
                    if ticket.dni:
                        count = Ticket.objects.filter(dni = key).count()
                    else:
                        count = Ticket.objects.filter(phone_number = key).count()
                    if key not in buyers:
                        buyers[key] = {
                            "buyer_name": ticket.buyer_name,
                            "dni": ticket.dni,
                            "phone_number": ticket.phone_number,
                            'email': ticket.email,
                            'numero_tickets': count,
                        }

            response['clients'] = buyers

            return Response(buyers, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)