# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
from useraccount.models import User,Token
from django.conf import settings
from django.core.mail import send_mail


def send_mail_to_user(email): 
    user=User.objects.get(email=email)
    user_id =user.id
    user_token=Token.objects.create(user=user)
    subject="Verifyyy"
    message=f"Verify Your Email in  http://localhost:8000/user/verify/{user_token}  Dont share this link to anyone"
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email] 
    send_mail(subject,message,from_email,recipient_list)