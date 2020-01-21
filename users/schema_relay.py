
from django.contrib.auth import get_user_model

import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation


from .models import Property, PropertyAddress, Buyer, EnergySource, Payment, BillingAddress
from .serializers import EnergySourceSerializers, PropertySerializer, PaymentSerializer, BilliingAddressSerializer
from users.models import User, UserOTP

from graphql_jwt.decorators import login_required


class PropertyNode(DjangoObjectType):

    class Meta:
        model = Property
        filter_fields = ["owner", "property_type"]
        interfaces = (graphene.relay.Node, )
        permissions = [login_required]


class PropertyAddressNode(DjangoObjectType):
    class Meta:
        model = PropertyAddress
        interfaces = (graphene.relay.Node, )
        permissions = [login_required]


class BuyerNode(DjangoObjectType):

    class Meta:
        model = Buyer
        filter_fields = ["user", "id"]
        interfaces = (graphene.relay.Node, )
        permissions = [login_required]


class EnergySourceNode(DjangoObjectType):

    class Meta:
        model = EnergySource
        interfaces = (graphene.relay.Node, )
        permissions = [login_required]


class UserNode(DjangoObjectType):

    class Meta:
        model = get_user_model()
        interfaces = (graphene.relay.Node, )
        permissions = [login_required]


class PaymentNode(DjangoObjectType):

    class Meta:
        model = Payment
        filter_fields = []
        interfaces = (graphene.relay.Node, )


class BillingAddressNode(DjangoObjectType):

    class Meta:
        model = BillingAddress
        filter_fields = []
        interfaces = (graphene.relay.Node, )


class EnergeySourceSerializerMutation(SerializerMutation):

    class Meta:
        serializer_class = EnergySourceSerializers
        model_operations = ['create', 'update']
        lookup_field = 'id'


class PropertySerializerMutation(SerializerMutation):

    class Meta:
        serializer_class = PropertySerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):

        if 'id' in input:
            input.pop("property_address")
            instance = Property.objects.filter(
                id=input['id']
            ).first()
            if instance:
                return {'instance': instance, 'data': input, 'partial': True}

            else:
                raise http.Http404

        return {'data': input, 'partial': True}

    @classmethod
    def perform_mutate(cls, serializer, info):
        if not info.context.user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        obj = serializer.save()
        kwargs = {}
        for f, field in serializer.fields.items():
            if not field.write_only:
                kwargs[f] = field.get_attribute(obj)

        return cls(errors=None, **kwargs)


class BillingAddressSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = BilliingAddressSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


class PaymentSerializerMutation(SerializerMutation):

    class Meta:
        serializer_class = PaymentSerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):

        if 'id' in input:
            input.pop("property_address")
            instance = Property.objects.filter(
                id=input['id']
            ).first()
            if instance:
                return {'instance': instance, 'data': input, 'partial': True}

            else:
                raise http.Http404

        return {'data': input, 'partial': True}

    @classmethod
    def perform_mutate(cls, serializer, info):
        if not info.context.user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        obj = serializer.create(serializer.validated_data, info.context.user)
        kwargs = {}
        for f, field in serializer.fields.items():
            if not field.write_only:
                kwargs[f] = field.get_attribute(obj)

        return cls(errors=None, **kwargs)


class RelayQuery(graphene.ObjectType):
    relay_property = graphene.relay.Node.Field(PropertyNode)
    relay_properties = DjangoFilterConnectionField(PropertyNode)

    buyer = graphene.relay.Node.Field(BuyerNode)
    buyers = DjangoFilterConnectionField(BuyerNode)

    payments = DjangoFilterConnectionField(PaymentNode)


class RelayMutate(graphene.ObjectType):
    create_energy_source = EnergeySourceSerializerMutation.Field()
    create_property = PropertySerializerMutation.Field()

    create_billing_address = BillingAddressSerializerMutation.Field()
    create_payment = PaymentSerializerMutation.Field()
