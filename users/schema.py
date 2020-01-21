from django.db import transaction
from django.utils import timezone

from users.models import User, UserOTP, Buyer

from seller.models import Seller


import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from users.otp_generator import CreateUserOTP

# This is the class for defining user type


class UserType(DjangoObjectType):
    class Meta:
        model = User


# This is the mutaion for user creation
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone_no = graphene.String(required=True)
        is_buyer = graphene.Boolean(required=True)
        is_seller = graphene.Boolean(required=True)

    @transaction.atomic
    def mutate(self, info, username, password, email, first_name, last_name, is_buyer, is_seller, phone_no):
        user = User(
            username=username,
            email=email,
            phone_no=phone_no,
            is_buyer=is_buyer,
            is_seller=is_seller,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        if user.is_buyer:
            Buyer.objects.create(user=user)
        if user.is_seller:
            Seller.objects.create(user=user)
        user_otp = CreateUserOTP(user.id)
        user_otp.generate()
        # user_otp.send_mail(email)

        return CreateUser(user=user)


# This is the mutation for sending Otp
class SendOtp(graphene.Mutation):
    sent = graphene.Boolean()

    class Arguments:
        email = graphene.String(required=False)
        phone_no = graphene.String(required=False)
        resend = graphene.Boolean()

    def mutate(self, info, email=None, phone_no=None, resend=False):
        if resend:
            if not(email or phone_no):
                SendOtp(sent=False)
            else:
                if email:
                    user_otp = UserOTP.objects.get(user__email=email)
                    otp = CreateUserOTP(user_otp.user.id)
                    code = otp.generate_new()
                    print(code)
                    user_otp.code = code
                    user_otp.date_created = timezone.now()
                    user_otp.save()
                    user_otp.send_mail()
                    return SendOtp(sent=True)
        else:
            if phone_no or email:
                if phone_no:
                    return SendOtp(sent=False)
                elif email:
                    otp = UserOTP.objects.get(user__email=email)
                    print(otp)
                    otp.send_mail()
                    return SendOtp(sent=True)

        return SendOtp(sent=False)

# This is the class for verifying Otp


class VerifyOTP(graphene.Mutation):
    verified = graphene.Boolean()
    user = graphene.Field(UserType)

    class Arguments:  # Two arguments for verfiying otp
        otp = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, otp, email):
        try:
            user = User.objects.get(email=email)
            user_otp = UserOTP.objects.get(user=user)
        except Exception as e:
            raise Exception('User does not exist')

        # if user_otp.code != otp:
        #     raise Exception('Code does not match')

        if user_otp.validate(otp):
            user.is_active = True
            user.is_verified = True
            user.save()
            return VerifyOTP(verified=True, user=user)
        return VerifyOTP(verified=False)


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    @login_required
    def resolve_users(self, info):
        return User.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    verify_otp = VerifyOTP.Field()
    send_otp = SendOtp.Field()
