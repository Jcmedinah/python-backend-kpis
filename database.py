from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://5416f62cf0029e8b3393bc2ad9c920291f7cc56618ec6ff80d1d4f5ddf44aeb0:sk_J6cF1uqrjcBw3oD8K7MrS@pooled.db.prisma.io:5432/postgres?sslmode=require"
)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, index=True)

class Article(Base):
    __tablename__ = "articles"
    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    quantity_available = Column(Integer)
    quantity_total = Column(Integer)
    quantity_damaged = Column(Integer)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    user_role = Column(String)

class Loan(Base):
    __tablename__ = "loans"
    loan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    item_id = Column(Integer, ForeignKey("articles.item_id"))
    loan_date = Column(Date)
    due_date = Column(Date)
    return_date = Column(Date, nullable=True)
    status = Column(String)
