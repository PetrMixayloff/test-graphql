import graphene
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from serializers import *
from models import Users, Transaction, session_scope

# - mutation на добавление пользователя
# - mutation на добавление транзакции
# - query на список пользователей
# - query на пользователя по ID или email
# - query на баланс пользователя
# - query на список транзакций


class Query(graphene.ObjectType):
    list_users = graphene.List(UserGrapheneModel)
    list_user_transactions = graphene.List(TransactionGrapheneModel, user_id=graphene.NonNull(graphene.Int))
    get_user_by_id_or_email = graphene.Field(UserGrapheneModel, user_id=graphene.Int(required=False, default_value=None),
                                             user_email=graphene.String(required=False, default_value=None))

    @staticmethod
    def resolve_list_users(parent, info):
        with session_scope() as session:
            users = session.query(Users)
        return users.all()

    @staticmethod
    def resolve_list_user_transactions(parent, info, user_id):
        with session_scope() as session:
            transactions = session.query(Transaction).filter(Transaction.user_id == user_id)
        return transactions.all()

    @staticmethod
    def resolve_get_user_by_id_or_email(parent, info, user_id, user_email):
        with session_scope() as session:
            if user_id is not None and user_email is not None:
                return session.query(Users).filter(Users.id == user_id, Users.email == user_email).first()
            elif user_id is not None:
                return session.query(Users).filter(Users.id == user_id).first()
            elif user_email is not None:
                return session.query(Users).filter(Users.email == user_email).first()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_details = UserGrapheneInputModel()

    Output = UserGrapheneModel

    @staticmethod
    def mutate(parent, info, user_details):
        user_in = jsonable_encoder(user_details)
        user = Users(**user_in)
        with session_scope() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user


class CreateTransaction(graphene.Mutation):
    class Arguments:
        transaction_details = TransactionGrapheneInputModel()

    Output = TransactionGrapheneModel

    @staticmethod
    def mutate(parent, info, transaction_details):
        transaction_in = jsonable_encoder(transaction_details)
        transaction = Transaction(**transaction_in)
        with session_scope() as session:
            user = session.query(Users).filter(Users.id == transaction.user_id).first()
            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail="User hasn't found for transaction.",
                )
            user.balance += transaction.sum
            session.add(transaction)
            session.add(user)
            session.commit()
            session.refresh(transaction)
            session.refresh(user)
        return transaction


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_transaction = CreateTransaction.Field()
