from django.utils import timezone

from django.contrib.auth import get_user_model
from users.models import UserOTP
from django.core.mail import send_mail

import random

# This is the function to generate five digit code


def genetate_opt():
    otp_code = random.randrange(11111, 99999)
    return otp_code

# This is the class for generating user code and saving it


class CreateUserOTP:
    def __init__(self, user_id, code=None):
        self.user = get_user_model().objects.get(id=user_id)
        self.code = code
    # This class method creates code and return UserOTP model object

    def generate(self):
        # user = get_user_model().objects.get(id=self.user_id)
        self.code = genetate_opt()
        otp = UserOTP.objects.create(
            user=self.user, code=self.code, date_created=timezone.now())
        return otp

    @staticmethod
    def generate_new():
        return genetate_opt()

    # This method will send mail to
    def send_mail(self, email):
        message = "Your activation code is %d" % (self.code)
        send_mail(
            'Activation Code',
            message,
            'supportp2p@yopmail.com',
            [email],
            fail_silently=False,
        )
