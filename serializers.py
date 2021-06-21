from graphene_pydantic import PydanticInputObjectType, PydanticObjectType
from pydantic import BaseModel
from datetime import datetime, timezone


class UserModel(BaseModel):
    id: int
    name: str
    email: str
    balance: float = 0.00

    class Config:
        orm_mode = True


class TransactionModel(BaseModel):
    id: int
    user_id: int
    sum: float
    date: datetime

    class Config:
        orm_mode = True


class UserGrapheneModel(PydanticObjectType):
    class Meta:
        model = UserModel


class TransactionGrapheneModel(PydanticObjectType):
    class Meta:
        model = TransactionModel


class UserGrapheneInputModel(PydanticInputObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ('id', 'balance')


class TransactionGrapheneInputModel(PydanticInputObjectType):
    class Meta:
        model = TransactionModel
        exclude_fields = ('id', 'date')
