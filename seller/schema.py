from django.contrib.auth import get_user_model

import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation

from users.schema_relay import UserNode

from .models import Seller, SellerAddress, PaymentMethod, EnergyDetail
from .serializers import EnergyDetailSerializer

from graphql_jwt.decorators import login_required


class SellerNode(DjangoObjectType):

    class Meta:
        model = Seller
        filter_fields = ["user__username", "id"]
        interfaces = (graphene.relay.Node, )


class SellerAddressNode(DjangoObjectType):

    class Meta:
        model = SellerAddress
        filter_fields = ["id"]
        interfaces = (graphene.relay.Node, )


class PaymentMethodNode(DjangoObjectType):

    class Meta:
        model = PaymentMethod
        filter_fields = ["id"]
        interfaces = (graphene.relay.Node, )


class EnergyDetailNode(DjangoObjectType):

    class Meta:
        model = EnergyDetail
        filter_fields = ["id"]
        interfaces = (graphene.relay.Node, )


class EnergyDetailMutation(SerializerMutation):

    class Meta:
        serializer_class = EnergyDetailSerializer
        model_operations = ['create', 'update']

    @classmethod
    def perform_mutate(cls, serializer, info):
        if not info.context.user.is_authenticated:
            raise Exception('Authentication credentials were not provided')
        obj = serializer.create(serializer.validated_data,
                                info.context.user.seller)
        kwargs = {}
        for f, field in serializer.fields.items():
            if not field.write_only:
                try:
                    if field.many:
                        kwargs[f] = field.get_attribute(obj).all()

                except Exception as e:
                    kwargs[f] = field.get_attribute(obj)

        return cls(errors=None, **kwargs)


class RelayQuery(graphene.ObjectType):

    seller = graphene.relay.Node.Field(SellerNode)
    sellers = DjangoFilterConnectionField(SellerNode)

    energy = graphene.relay.Node.Field(EnergyDetailNode)
    energies = DjangoFilterConnectionField(EnergyDetailNode)


class RelayMutation(graphene.ObjectType):
    create_energy = EnergyDetailMutation.Field()
