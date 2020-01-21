from rest_framework import serializers

from .models import EnergySource, Property, PropertyAddress, Buyer, BillingAddress, Payment


class EnergySourceSerializers(serializers.ModelSerializer):

    class Meta:
        model = EnergySource
        fields = "__all__"

    # def create(self, *args, **kwargs):
    #     print("hello")
    #     return EnergySource.objects.all()[0]


class PropertyAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyAddress
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Buyer.objects.all(),
        write_only=True
    )
    property_address = PropertyAddressSerializer()
    prefered_energy = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = Property
        fields = ['id', 'property_type', 'property_name',
                  'meter', 'avg_consumption', 'buy_percent',
                  'owner', 'property_address', "prefered_energy"]

    def create(self, validated_data):
        property_address_data = validated_data.pop("property_address")
        prefered_energy = validated_data.pop("prefered_energy")
        owner = validated_data.get("owner")
        for key in prefered_energy:
            owner.prefered_energy.add(key)
        property_address = PropertyAddress.objects.create(
            **property_address_data)
        propty = Property.objects.create(
            property_address=property_address,  **validated_data)
        # propty = Property.objects.all().first()
        return propty


class BilliingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingAddress
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):

    bill_address = BilliingAddressSerializer()

    class Meta:
        model = Payment
        fields = ['name_card', 'card_number',
                  'vlaid_till', 'verification_code', "bill_address"]

    def create(self, validated_data, user):
        address = validated_data.pop("bill_address")
        billing_address = BillingAddress.objects.create(**address)
        payment = Payment.objects.create(
            **validated_data, user=user, bill_address=billing_address)
        return payment
