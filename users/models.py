from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.mail import send_mail

from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

from django.utils import timezone


class User(AbstractUser):
    phone_no = models.CharField(max_length=50,  unique=True)
    email = models.EmailField(max_length=254, unique=True)
    is_buyer = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


class UserOTP(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    code = models.CharField(max_length=5, validators=[MinLengthValidator(5)])
    date_created = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("UserOTP")
        verbose_name_plural = ("UserOTPs")

    def __str__(self):
        return str(self.code)

    def get_absolute_url(self):
        return reverse("UserOTP_detail", kwargs={"pk": self.pk})

    def validate(self, otp, *args, **kwargs):
        if timezone.now() > (self.date_created + timezone.timedelta(hours=1)):
            self.is_active = False
            super(UserOTP, self).save(*args, **kwargs)
            return False
        elif self.code != otp:
            return False

        return True

    def send_mail(self):
        message = "Your activation code is %s" % (self.code)
        send_mail(
            'Activation Code',
            message,
            'supportp2p@yopmail.com',
            [self.user.email],
            fail_silently=False,
        )

# class UserProfile(models.Model):

#     phone_no = models.CharField(max_length=50)

#     class Meta:
#         verbose_name = ("UserProfile")
#         verbose_name_plural = ("UserProfiles")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("UserProfile_detail", kwargs={"pk": self.pk})


class PropertyAddress(models.Model):

    name_bill = models.CharField(max_length=500)
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Property Address")
        verbose_name_plural = ("Property Addresses")

    def __str__(self):
        return self.name_bill

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})


class EnergySource(models.Model):
    # ENERGY_SOURCES = [
    #     ('so', 'Solar'),
    #     ('wi', 'Wind'),
    #     ('ge', 'Geo'),
    #     ('ba', 'Battery')
    # ]

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = ("EnergySource")
        verbose_name_plural = ("Energy Sources")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("EnergySource_detail", kwargs={"pk": self.pk})


class Buyer(models.Model):

    ENERGY_SOURCES = [
        ('so', 'Solar'),
        ('wi', 'Wind'),
        ('ge', 'Geo'),
        ('ba', 'Battery')
    ]

    user = models.OneToOneField(
        "users.User", verbose_name=("User"), on_delete=models.CASCADE)

    prefered_energy = models.ManyToManyField(
        "users.EnergySource")
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Buyer")
        verbose_name_plural = ("Buyers")

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse("Buyer_detail", kwargs={"pk": self.pk})


class Property(models.Model):
    PROPERTY_CHOICES = [
        ("RE", 'Residential'),
        ("CO", "Commercial")
    ]

    owner = models.ForeignKey("users.Buyer", verbose_name=(
        "Buyers"), on_delete=models.CASCADE)
    property_type = models.CharField(max_length=2, choices=PROPERTY_CHOICES)
    property_name = models.CharField(("Property name"), max_length=500)
    meter = models.CharField(max_length=50)
    avg_consumption = models.CharField(
        ("Average energy consumption/month"), max_length=50)
    property_address = models.ForeignKey(
        "users.PropertyAddress", verbose_name=("property address"),
        on_delete=models.CASCADE, null=True, blank=True)
    buy_percent = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = ("Property")
        verbose_name_plural = ("Properties")

    def __str__(self):
        return self.property_name

    def get_absolute_url(self):
        return reverse("Property_detail", kwargs={"pk": self.pk})


class BillingAddress(models.Model):

    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("BillingAddress")
        verbose_name_plural = ("BillingAddresss")

    def __str__(self):
        return self.address1

    def get_absolute_url(self):
        return reverse("BillingAddress_detail", kwargs={"pk": self.pk})


class Payment(models.Model):

    CARD_TYPE = [
        ("cr", "Credit Card"),
        ('ma', "Master Card"),
        ("vi", "Visa Card"),
    ]

    user = models.ForeignKey(get_user_model(), verbose_name=(
        "User"), on_delete=models.CASCADE)
    name_card = models.CharField(max_length=500)
    card_number = models.CharField(max_length=50)
    vlaid_till = models.DateField()
    verification_code = models.CharField(max_length=50)
    bill_address = models.ForeignKey(
        "users.BillingAddress", verbose_name=("Billig Address"),
        on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = ("Payment")
        verbose_name_plural = ("Payments")

    def __str__(self):
        return self.name_card

    def get_absolute_url(self):
        return reverse("Payment_detail", kwargs={"pk": self.pk})
