from django.urls import path
from .views import (RegisterView, LoginView, 
                   UserListView, UserRetrieveView,
                   SorteoListView, SorteoDetailView,
                   ObjetoListView, ObjetoDetailView,
                   TicketListView, TicketDetailView,
                   SorteoView,
                   )
urlpatterns = [
        path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),  
    path('users/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'), 

    path('sorteos/', SorteoListView.as_view(), name='sorteo-list-create'),
    path('sorteos/<int:pk>/', SorteoDetailView.as_view(), name='sorteo-detail'),

    path('objetos/', ObjetoListView.as_view(), name='objetos-list-create'),
    path('objetos/<int:pk>/', ObjetoDetailView.as_view(), name='objetos-detail'),

    path('tickets/', TicketListView.as_view(), name='tickets-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='tickets-detail'),

    path('hacer-sorteo/', SorteoView.as_view(), name='hacer-sorteo'),
]