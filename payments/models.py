from django.db import models
from django.conf import settings



class Status(models.TextChoices):
    credit="credit","CREDIT"
    debit="debit","DEBIT"

class PaymentHistory(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    from_account=models.IntegerField()
    to_account=models.IntegerField()
    status=models.CharField(max_length=15,choices=Status.choices)
    amount=models.CharField(max_length=255,default=0)
    transation_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
