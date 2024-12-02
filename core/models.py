from django.db import models
from django.contrib.auth.models import User

class Raffle(models.Model):
    ticket_limit = models.IntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    public_name = models.CharField(max_length=50, null=True, unique=True)
    description = models.TextField(max_length=500, null=True)
    image = models.CharField(max_length=500, null=True)
    ticket_price = models.FloatField(null=True)
    raffle_date = models.DateTimeField(null=True)
    raffleNumber = models.CharField(null=True)

    def save(self, *args, **kwargs):

        lastRaffle = Raffle.objects.filter(id = self.id, user__id=self.user.id).first()

        if not lastRaffle or not lastRaffle.raffleNumber:
            self.raffleNumber = 'RF1'
        else:
            lastRaffleNumber = int(lastRaffle.raffleNumber.split('F')[1])
            self.raffleNumber = f'RF{lastRaffleNumber+1}'

        super().save(*args, **kwargs)
    

class Ticket(models.Model):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100, null=True)
    dni = models.CharField(max_length=10, null= True)
    email = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    sale_date = models.DateTimeField(null=True)
    total_paid = models.FloatField(default=0.00)
    ticketNumber = models.IntegerField(null=True, blank=True)
    codigo = models.CharField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['raffle', 'ticketNumber'], name='unique_ticket_per_raffle')
        ]

    def save(self, *args, **kwargs):
        if not self.ticketNumber:
            # Get the last ticket for the same raffle and increment its ticketNumber
            last_ticket = Ticket.objects.filter(raffle=self.raffle).order_by('-ticketNumber').first()
            self.ticketNumber = 1 if not last_ticket or not last_ticket.ticketNumber else last_ticket.ticketNumber + 1
        if not self.codigo:
            self.codigo = self.get_codigo()
        super().save(*args, **kwargs)
    
    def get_codigo(self):
        if hasattr(self.raffle, 'raffleNumber'):
            return f'{self.raffle.raffleNumber}-{self.ticketNumber}'
        return f'RAFFLE-{self.raffle.id}-{self.ticketNumber}'


class Prize(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=500, null=True)
    image = models.CharField(max_length=500, null=True)

class PrizeRaffle(models.Model):
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    winnerTicket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    sorted = models.BooleanField(default=False)
