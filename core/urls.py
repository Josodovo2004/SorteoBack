from django.urls import path
from .views import (RegisterView, LoginView, 
                   UserListView, UserRetrieveView,
                   SorteoListView, SorteoDetailView,
                   PremioListView, PremioDetailView,
                   TicketListView, TicketDetailView,
                   SorteoView,
                   PremioSorteoDetailView, PremioSorteoListCreateView,
                   CustomTokenObtainPairView, CustomTokenRefreshView
                   )
urlpatterns = [
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),  
    path('users/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'), 

    path('sorteos/', SorteoListView.as_view(), name='sorteo-list-create'),
    path('sorteos/<int:pk>/', SorteoDetailView.as_view(), name='sorteo-detail'),

    path('premios/', PremioListView.as_view(), name='premios-list-create'),
    path('premios/<int:pk>/', PremioDetailView.as_view(), name='premios-detail'),

    path('tickets/', TicketListView.as_view(), name='tickets-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='tickets-detail'),
    
    path('premio-sorteo/', PremioSorteoListCreateView.as_view(), name='premio-sorteo-list-create'),
    path('premio-sorteo/<int:pk>/', PremioSorteoDetailView.as_view(), name='premio-sorteo-detail'),

    path('hacer-sorteo/', SorteoView.as_view(), name='hacer-sorteo'),
]