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
    buyer_name = filters.CharFilter(lookup_expr='icontains')  # Case-insensitive contains
    email = filters.CharFilter(lookup_expr='icontains')
    phone_number = filters.CharFilter(lookup_expr='icontains')
    is_active = filters.BooleanFilter()
    is_paid = filters.BooleanFilter()
    sale_date = filters.DateFromToRangeFilter()  # Filter by date range
    total_paid = filters.RangeFilter()  # Filter by numeric range
    ticketNumber = filters.NumberFilter()
    codigo = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ticket
        fields = ['raffle', 'buyer_name', 'dni', 'email', 'phone_number', 
                  'is_active', 'is_paid', 'sale_date', 'total_paid', 
                  'ticketNumber', 'codigo']


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
