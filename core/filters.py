from django.contrib.auth.models import User
import django_filters as filters
from .models import Raffle, Ticket, Prize, PrizeRaffle


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    is_active = filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']


class RaffleFilter(filters.FilterSet):
    min_ticket_price = filters.NumberFilter(field_name="ticket_price", lookup_expr="gte")
    max_ticket_price = filters.NumberFilter(field_name="ticket_price", lookup_expr="lte")
    raffle_date = filters.DateTimeFilter(field_name="raffle_date", lookup_expr="exact")
    raffle_date_range = filters.DateFromToRangeFilter(field_name="raffle_date")

    class Meta:
        model = Raffle
        fields = ['user', 'name', 'public_name', 'min_ticket_price', 'max_ticket_price', 'raffle_date', 'raffle_date_range']


class TicketFilter(filters.FilterSet):
    is_winner = filters.BooleanFilter(field_name="is_winner")
    is_active = filters.BooleanFilter(field_name="is_active")
    is_paid = filters.BooleanFilter(field_name="is_paid")
    sale_date_range = filters.DateFromToRangeFilter(field_name="sale_date")
    total_paid_min = filters.NumberFilter(field_name="total_paid", lookup_expr="gte")
    total_paid_max = filters.NumberFilter(field_name="total_paid", lookup_expr="lte")

    class Meta:
        model = Ticket
        fields = ['raffle', 'is_winner', 'is_active', 'is_paid', 'sale_date_range', 'total_paid_min', 'total_paid_max']


class PrizeFilter(filters.FilterSet):
    class Meta:
        model = Prize
        fields = ['name', 'description']

class PrizeRaffleFilter(filters.FilterSet):
    sorted = filters.BooleanFilter(field_name="sorted")
    raffle = filters.ModelChoiceFilter(queryset=Raffle.objects.all())
    prize = filters.ModelChoiceFilter(queryset=Prize.objects.all())
    winner_ticket = filters.ModelChoiceFilter(queryset=Ticket.objects.all())

    class Meta:
        model = PrizeRaffle
        fields = ['raffle', 'prize', 'winnerTicket', 'sorted']
