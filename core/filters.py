from django.contrib.auth.models import User
import django_filters
from .models import Sorteo, Ticket, Objeto


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']




class SorteoFilter(django_filters.FilterSet):
    usuario__user__username = django_filters.CharFilter(lookup_expr='icontains')
    limiteTickets = django_filters.NumberFilter()

    class Meta:
        model = Sorteo
        fields = ['usuario__user__username', 'limiteTickets']


class TicketFilter(django_filters.FilterSet):
    sorteo__id = django_filters.NumberFilter(field_name='sorteo__id')
    usuario__user__username = django_filters.CharFilter(lookup_expr='icontains')
    precio = django_filters.RangeFilter()  # Allows filtering by price range (e.g., min and max)

    class Meta:
        model = Ticket
        fields = ['sorteo__id', 'usuario__user__username', 'precio']


class ObjetoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Objeto
        fields = ['nombre']
