from app.models import Category, Product, User, Receipt, ReceiptDetail, UserRole
from app import app, db
import hashlib
from flask_login import current_user
from sqlalchemy import func


def load_category():
    return Category.query.all()


def load_product(kw=None, cate_id=None, page=None):
    products = Product.query
    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = products.filter(Product.name.contains(kw))

    page_size = app.config['PAGE_SIZE']
    start = page * page_size - page_size
    end = start + page_size

    return products.slice(start, end).all()


def count_products(kw=None, cate_id=None):
    count = Product.query.count()
    if cate_id:
        count = Product.query.filter(Product.category_id.__eq__(cate_id)).count()
    if kw:
        count = Product.query.filter(Product.name.contains(kw)).count()
    return count


def check_user_existence(username=None):
    user = User.query.filter_by(username=username).first()  # SELECT username FROM User WHERE username = @username
    if user:
        return True  # username's already existed in database
    return False  # username doesn't exist in database


def add_user(fullname=None, email=None, username=None, password=None, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(full_name=fullname.strip(),
                email=email.strip(),
                username=username.strip(),
                password=password,
                avatar=avatar)
    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id=None):
    return User.query.get(user_id)


def check_user_login(username, password, user_role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        user = User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(user_role)).first()

        return user


def count_cart(cart=None):
    total_quantity, total_amt = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amt += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amt': total_amt
    }


def pay_cart(cart=None):
    if cart and current_user:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)
        for c in cart.values():
            receipt_detail = ReceiptDetail(receipt=receipt,
                                           product_id=c['id'],
                                           quantity=c['quantity'],
                                           price=c['price'] * c['quantity'])
            db.session.add(receipt_detail)
        db.session.commit()


def category_stats():
    #     SELECT c.id, c.name, count(p.id)
    #     FROM Category c
    #     LEFT JOIN Product p
    #     ON c.id = p.category_id
    #     GROUP BY c.id, c.name
    with app.app_context():
        # cate_sts = Category.query.join(Product, Product.category_id.__eq__(Category.id), isouter=True).add_columns(
        #     func.count(Product.id)).group_by(Category.id, Category.name).all()
        cate_sts = db.session.query(Category.id, Category.name, func.count(Product.id)).join(
            Product, Category.id.__eq__(Product.category_id), isouter=True).group_by(Category.id, Category.name).all()

    return cate_sts


print(category_stats())
