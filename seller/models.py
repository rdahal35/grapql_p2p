from django.db import models
from django.contrib.auth import get_user_model


class Seller(models.Model):

    user = models.OneToOneField(
        get_user_model(), verbose_name=("User"), on_delete=models.CASCADE)

    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Seller")
        verbose_name_plural = ("Sellers")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Seller_detail", kwargs={"pk": self.pk})


class SellerAddress(models.Model):
    seller = models.ForeignKey(
        "seller.Seller", on_delete=models.CASCADE)
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("SellerAddress")
        verbose_name_plural = ("SellerAddresss")

    def __str__(self):
        return self.address1

    def get_absolute_url(self):
        return reverse("SellerAddress_detail", kwargs={"pk": self.pk})


class PaymentMethod(models.Model):
    METHODS = [
        ("Pa", "Paypal"),
        ("Cr", "Credit Card"),
        ("Cp", "Crypto"),
        ("P2P", "P2P Token")
    ]

    name = models.CharField(max_length=50, choices=METHODS)

    class Meta:
        verbose_name = ("PaymentMethod")
        verbose_name_plural = ("PaymentMethods")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PaymentMethod_detail", kwargs={"pk": self.pk})


class EnergyDetail(models.Model):

    PAYMENT_CHOICES = [
        ("Fi", "Fixed"),
        ("In", "Installment")
    ]
    seller = models.ForeignKey(
        "seller.Seller", verbose_name=("Seller"), on_delete=models.CASCADE)

    energy_source = models.OneToOneField(
        "users.EnergySource", on_delete=models.SET_NULL,
        null=True, blank=True)
    name = models.CharField(max_length=500)
    supplier = models.CharField(max_length=500)
    net_meter = models.CharField(max_length=50)
    avg_production = models.DecimalField(max_digits=10, decimal_places=2)
    sell_percent = models.DecimalField(max_digits=4, decimal_places=2)
    payment_duration = models.IntegerField()
    payment_type = models.CharField(max_length=2, choices=PAYMENT_CHOICES)
    price_kwh = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method = models.ManyToManyField(
        "seller.PaymentMethod", verbose_name=("Payment Methods"))
    address = models.ForeignKey(
        "seller.SellerAddress", verbose_name=("Address"), on_delete=models.SET_NULL,
        null=True, blank=True)

    class Meta:
        verbose_name = ("EnergyDetail")
        verbose_name_plural = ("EnergyDetails")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("EnergyDetail_detail", kwargs={"pk": self.pk})
