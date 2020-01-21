from django.contrib.auth import get_user_model

import graphene
import graphql_jwt

from graphql_jwt.mutations import JSONWebTokenMutation
from graphql_jwt.decorators import token_auth


import users.schema
import users.schema_relay
import seller.schema
from users.schema import UserType


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({
            get_user_model().USERNAME_FIELD: graphene.String(required=False),
            'password': graphene.String(required=True),
            "email": graphene.String(required=False),
        })
        return super(JSONWebTokenMutation, cls).Field(*args, **kwargs)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        print("hello")
        return cls(user=info.context.user)


class Verify(graphql_jwt.Verify):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Query(users.schema.Query,
            users.schema_relay.RelayQuery, seller.schema.RelayQuery, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, users.schema_relay.RelayMutate,
               seller.schema.RelayMutation, graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
