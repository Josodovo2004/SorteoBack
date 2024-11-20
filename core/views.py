from rest_framework.response import Response
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer, LoginSerializer, PremioSorteoSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from core.models import Sorteo, Ticket, Premio, PremioSorteo
from .filters import UserFilter, TicketFilter, SorteoFilter, PremioFilter
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, SorteoSerializer, PremioSerializer, TicketSerializer, CustomTicketSerializer
from django_filters.rest_framework import DjangoFilterBackend
import random
from rest_framework.permissions import IsAuthenticated



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_summary="User registration",
        operation_description="Registers a new user with the provided data.",
        responses={201: openapi.Response("Created", schema=RegisterSerializer)}
    )
    def post(self, request, *args, **kwargs):
        """
        Registers a new user.
        """
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
        user = serializer.validated_data['user']  # Get the authenticated user

        # Generate tokens using the CustomTokenObtainPairView logic
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        # Set the refresh token in a secure cookie
        response = Response({
            'access': access,
        }, status=status.HTTP_200_OK)

        # Set the refresh token in an HttpOnly, Secure cookie
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,  # Ensure the cookie is sent over HTTPS
            samesite='Lax',
            max_age=60 * 60 * 24 * 7  # 1 week
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

        # Here you can add additional response data if needed
        response.data['custom_message'] = 'Welcome!'

        # Set the refresh token in an HttpOnly, Secure cookie
        refresh_token = response.data['refresh']
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,   # Prevents JavaScript access
            samesite='Lax',  # Adjust as necessary (can also use 'Strict')
            max_age=60 * 60 * 24 * 7  # 1 week
        )

        return response
    
    
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token not found.'}, status=401)

        # Pass the refresh token from the cookie to the super method
        data = {'refresh': refresh_token}
        request.data['refresh'] = refresh_token
        return super().post(request, *args, **kwargs)
    
class SorteoListView(generics.ListCreateAPIView):
    queryset = Sorteo.objects.all()
    serializer_class = SorteoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SorteoFilter


class SorteoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sorteo.objects.all()
    serializer_class = SorteoSerializer
    permission_classes = [IsAuthenticated]  # Require authentication



class TicketListView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TicketFilter


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]  # Require authentication



class PremioListView(generics.ListCreateAPIView):
    queryset = Premio.objects.all()
    serializer_class = PremioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PremioFilter


class PremioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Premio.objects.all()
    serializer_class = PremioSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
class PremioSorteoListCreateView(generics.ListCreateAPIView):
    queryset = PremioSorteo.objects.all()
    serializer_class = PremioSorteoSerializer
    
class PremioSorteoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PremioSorteo.objects.all()
    serializer_class = PremioSorteoSerializer


class SorteoView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve the winner of a specified Sorteo (raffle).",
        manual_parameters=[
            openapi.Parameter(
                'id_sorteo',
                openapi.IN_QUERY,
                description="ID of the Sorteo (raffle).",
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
                        'ganador': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Details of the winning ticket.",
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'precio': openapi.Schema(type=openapi.TYPE_NUMBER),
                                'usuario': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Details of the ticket holder."
                                ),
                                'sorteo': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    description="Details of the Sorteo (raffle)."
                                ),
                            },
                        ),
                    },
                ),
            ),
            400: "Bad Request: Missing or invalid parameters.",
            404: "Not Found: Sorteo or tickets not found.",
        },
    )
    def get(self, request):
        id_sorteo = request.query_params.get('id_sorteo')

        # Validate that id_sorteo is provided
        if not id_sorteo:
            return Response(
                {"error": "The 'id_sorteo' parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            id_sorteo = int(id_sorteo)
        except ValueError:
            return Response(
                {"error": "The 'id_sorteo' parameter must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch the Sorteo object
        sorteo = Sorteo.objects.filter(id=id_sorteo).first()
        if not sorteo:
            return Response(
                {"error": f"Sorteo with id {id_sorteo} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fetch tickets associated with the Sorteo
        lista_tickets = list(Ticket.objects.filter(sorteo=sorteo))
        if not lista_tickets:
            return Response(
                {"error": f"No tickets found for Sorteo with id {id_sorteo}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Shuffle tickets to pick a winner
        random.shuffle(lista_tickets)
        winnerNumber = random.randint(0, len(lista_tickets))
        ganador = lista_tickets[winnerNumber]

        # Mark the winning ticket
        ganador.ganador = True
        ganador.save()  # Save the update to the database

        # Serialize the winning ticket
        winner_ticket = CustomTicketSerializer(ganador).data

        return Response({'ganador': winner_ticket}, status=status.HTTP_200_OK)