from rest_framework import serializers

from .models import Seller, SellerAddress, PaymentMethod, EnergyDetail
from users.serializers import EnergySourceSerializers


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['id', "date_joined"]


class SellerAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerAddress
        exclude = ['seller']


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = ['id', 'name']


class EnergyDetailSerializer(serializers.ModelSerializer):

    address = SellerAddressSerializer()
    energy_source = EnergySourceSerializers()
    payment_method = PaymentMethodSerializer(many=True)

    class Meta:
        model = EnergyDetail
        exclude = ['seller']

    def create(self, validated_data, seller):
        energy = EnergyDetail.objects.all().first()
        return energy
