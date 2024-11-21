from django.contrib.auth.models import User
import django_filters
from .models import Sorteo, Ticket, Premio, PremioSorteo


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']




class SorteoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    usuario = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    precioTickets_min = django_filters.NumberFilter(field_name="precioTickets", lookup_expr='gte')
    precioTickets_max = django_filters.NumberFilter(field_name="precioTickets", lookup_expr='lte')
    fechaSorteo = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Sorteo
        fields = ['nombre', 'nombrePublico', 'usuario', 'precioTickets', 'fechaSorteo']


class TicketFilter(django_filters.FilterSet):
    sorteo = django_filters.ModelChoiceFilter(queryset=Sorteo.objects.all())
    nombreComprador = django_filters.CharFilter(lookup_expr='icontains')
    correo = django_filters.CharFilter(lookup_expr='icontains')
    estado = django_filters.BooleanFilter()
    fechaVenta = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Ticket
        fields = ['sorteo', 'ganador', 'nombreComprador', 'correo', 'estado', 'fechaVenta']


class PremioFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Premio
        fields = ['nombre']



class PremioSorteoFilter(django_filters.FilterSet):
    premio = django_filters.ModelChoiceFilter(queryset=Premio.objects.all())
    sorteo = django_filters.ModelChoiceFilter(queryset=Sorteo.objects.all())

    class Meta:
        model = PremioSorteo
        fields = ['premio', 'sorteo']