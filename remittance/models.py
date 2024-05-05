from django.db import models
from useraccount.models import User,Status,PaymentChoices

# Create your models here.


class TransactionHistory(models.Model):
    '''This model is for esewa and khalti to load money'''
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="from_user")
    amount = models.DecimalField(max_digits=10,decimal_places=3)
    created=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15,choices=Status.choices)
    transaction_id = models.CharField(max_length=200)
    transaction_response = models.JSONField()
    transaction_type = models.CharField(max_length=100,choices=PaymentChoices.choices)

    def __str__(self):
        return f"{self.user.email} loaded {self.amount}"