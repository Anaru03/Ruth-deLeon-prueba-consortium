from django.db import models
from django.contrib.auth import get_user_model


class Spending(models.Model):
    class SPENDING_TYPE(models.TextChoices):
        INVOICED = 'INVOICED', 'Facturado'
        NOT_INVOICED = 'NOT_INVOICED', 'No Facturado'

    class STATUS(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        FINISHED = 'FINISHED', 'Finalizado'
        DELETED = 'DELETED', 'Eliminado'

    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='spendings_registered')
    created_at = models.DateTimeField(auto_now_add=True)
    liquidations = models.ManyToManyField(
        'Liquidation',
        related_name='spendings_registered')
    liquidation_sent = models.FileField(
        upload_to='liquidation_sent/',
        null=True, blank=True)
    account_status = models.FileField(
        upload_to='account_status/', null=True, blank=True)
    liquidation_certificate = models.FileField(
        upload_to='liquidation_certificate/', null=True, blank=True)
    signed_liquidation_certificate = models.FileField(
        upload_to='signed_liquidation_certificate/', null=True, blank=True)
    invoice = models.FileField(
        upload_to='invoice/', null=True, blank=True)
    type = models.CharField(
        max_length=100,
        choices=SPENDING_TYPE.choices,
        default=SPENDING_TYPE.NOT_INVOICED)
    status = models.CharField(
        max_length=100,
        choices=STATUS.choices,
        default=STATUS.PENDING)
    totals_match = models.BooleanField(default=True)
    justification = models.TextField(null=True, blank=True)

    @property
    def can_generate_liquidation_certificate(self):
        if self.type == self.SPENDING_TYPE.INVOICED:
            required_fields_present = all([
                self.liquidation_sent,
                self.account_status,
                self.invoice,
                (self.liquidation_certificate is None or self.liquidation_certificate == '')
            ])
        else:
            required_fields_present = all([
                self.liquidation_sent,
                self.account_status,
                (self.liquidation_certificate is None or self.liquidation_certificate == '')
            ])
        return required_fields_present

    def __str__(self):
        return f'Spending {self.id} - {self.description}'


class Liquidation(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Liquidation {self.id} - Amount: {self.amount}'