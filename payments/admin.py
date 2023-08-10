from django.contrib import admin
from payments.models import PaymentHistory

# Register your models here.
@admin.register(PaymentHistory)
class AdminPaymentHistory(admin.ModelAdmin):
    list_display=["user","from_account","to_account","status","amount","transation_date"]