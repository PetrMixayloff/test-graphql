from sqlalchemy import create_engine, Column, DateTime, String, ForeignKey, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from datetime import datetime

POSTGRES_DSN = "postgresql://test_graph_user:12345678@localhost:5432/test_graph"
engine = create_engine(POSTGRES_DSN, pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.00)


class Transaction(Base):
    __tablename__ = 'tranaction'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    sum = Column(Float)
    date = Column(DateTime, default=datetime.utcnow())
    user_id = Column(Integer, ForeignKey('users.id'))
