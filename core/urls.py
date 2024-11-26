from django.urls import path
from .views import (RegisterView, LoginView, 
                   UserListView, UserRetrieveView,
                   RaffleListView, RaffleDetailView,
                   PrizeListView, PrizeDetailView,
                   TicketView, TicketDetailView,
                   RaffleView, GetPaidTickets,
                   PrizeRaffleListView, PrizeRaffleCreateView, PrizeRaffleDetailView,
                   CustomTokenObtainPairView, CustomTokenRefreshView,
                   WinnersListApiView,
                   )
urlpatterns = [
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),  
    path('users/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'), 

    path('raffles/', RaffleListView.as_view(), name='raffles-list-create'),
    path('raffles/<int:pk>/', RaffleDetailView.as_view(), name='raffles-detail'),

    path('prizes/', PrizeListView.as_view(), name='prizes-list-create'),
    path('prizes/<int:pk>/', PrizeDetailView.as_view(), name='prizes-detail'),

    path('tickets/', TicketView.as_view(), name='tickets-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='tickets-detail'),
    
    path('prize-raffle-list/', PrizeRaffleListView.as_view(), name='prize-raffle-list-list'),
    path('prize-raffle-create/', PrizeRaffleCreateView.as_view(), name='price-raffle-create'),
    path('prize-raffle/<int:pk>/', PrizeRaffleDetailView.as_view(), name='prize-raffle-detail'),

    path('make-raffle/', RaffleView.as_view(), name='make-raffle'),

    path('paid-tickets/', GetPaidTickets.as_view(), name='paid-tickets'),

    path('raffle-winners/', WinnersListApiView.as_view(), name='raffle-winners')
]