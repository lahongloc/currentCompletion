from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Relationship
from app import app, db
from enum import Enum as UserEnum
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseModel, UserMixin):
    full_name = Column(String(30), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(500))
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = Relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.full_name


class Category(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    products = Relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0, nullable=False)
    image = Column(String(500))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = Relationship('ReceiptDetail', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt_details = Relationship('ReceiptDetail', backref='receipt', lazy=True)

    def __str__(self):
        return str(self.id)


class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)

    def __str__(self):
        return str(self.receipt_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # c1 = Category(name='Mobile')
        # c2 = Category(name='Tablet')
        #
        # db.session.add_all([c1, c2])
        # p1 = Product(name='iphone 12', price=12000000, category_id=1, image='https://s.net.vn/akTG')
        # p2 = Product(name='Ipad Pro 2022', price=20000000, category_id=2, image='https://s.net.vn/zrJ8')
        # p3 = Product(name='Samsung Glaxy S4', price=7000000, category_id=1, image='https://s.net.vn/WTWj')
        # db.session.add_all([p1, p2, p3])
        # db.session.commit()
