from django.contrib.auth.models import User
import django_filters
from .models import Raffle, Ticket, Prize, PrizeRaffle


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']


class RaffleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    ticket_price_min = django_filters.NumberFilter(field_name="ticket_price", lookup_expr='gte')
    ticket_price_max = django_filters.NumberFilter(field_name="ticket_price", lookup_expr='lte')
    draw_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Raffle
        fields = ['name', 'public_name', 'user', 'ticket_price', 'draw_date']


class TicketFilter(django_filters.FilterSet):
    raffle = django_filters.ModelChoiceFilter(queryset=Raffle.objects.all())
    buyer_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.BooleanFilter()
    sale_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Ticket
        fields = ['raffle', 'is_winner', 'buyer_name', 'email', 'status', 'sale_date']


class PrizeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Prize
        fields = ['name']


class PrizeRaffleFilter(django_filters.FilterSet):
    prize = django_filters.ModelChoiceFilter(queryset=Prize.objects.all())
    raffle = django_filters.ModelChoiceFilter(queryset=Raffle.objects.all())

    class Meta:
        model = PrizeRaffle
        fields = ['prize', 'raffle']
