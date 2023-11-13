from app import app
from flask import render_template, url_for, request, redirect, session, jsonify, flash
import utils
import math
import cloudinary.uploader
from app import login
from flask_login import login_user, logout_user, login_required
from app.models import UserRole


@app.route('/')
def home():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = int(request.args.get('page', 1))

    products = utils.load_product(kw=kw, cate_id=cate_id, page=page)
    page_number = math.ceil(utils.count_products(kw=kw, cate_id=cate_id) / app.config['PAGE_SIZE'])

    return render_template('index.html',
                           products=products,
                           page_number=page_number)


@app.context_processor
def common_response():
    return {
        'categories': utils.load_category(),
        'cart_status': utils.count_cart(session.get('cart'))
    }


@app.route('/register', methods=['post', 'get'])
def register():
    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')

        try:
            if not utils.check_user_existence(username=username):
                password = request.form.get('password')
                confirm_password = request.form.get('confirm')

                if password.strip().__eq__(confirm_password.strip()):
                    fullname = request.form.get('name')
                    email = request.form.get('email')
                    avatar = request.files.get('avatar')
                    avatar_path = None
                    if avatar:
                        res = cloudinary.uploader.upload(avatar)
                        avatar_path = res['secure_url']

                    utils.add_user(fullname=fullname,
                                   email=email,
                                   username=username,
                                   password=password,
                                   avatar=avatar_path)
                    return redirect(url_for('login'))
                else:
                    err_msg = 'Confirmed password does not MATCH!'
            else:
                err_msg = 'Username has already EXISTED!'
        except Exception as ex:
            err_msg = str(ex)
    if err_msg:
        flash(err_msg)
    return render_template('register.html')


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/user-login', methods=['post', 'get'])
def login():
    err_msg = None
    try:
        if request.method.__eq__('POST'):
            username = request.form.get('username')
            password = request.form.get('password')

            user = utils.check_user_login(username=username, password=password)
            if user:
                login_user(user=user)

                next_url = request.args.get('next', 'home')
                return redirect(url_for(next_url))
            else:
                err_msg = 'Username or password is incorrect!'
    except Exception as ex:
        err_msg = str(ex)

    if err_msg:
        flash(err_msg)
    return render_template('login.html')


@app.route('/user-logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    image = data.get('image')
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'image': image,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart
    cart_info = utils.count_cart(cart)

    return cart_info


@app.route('/cart')
def cart_detail():
    return render_template('cart.html')


@app.route('/cart', methods=['post'])
def delete_cart():
    del session['cart']
    return redirect('/cart')


@login_required
@app.route('/api/pay', methods=['post'])
def pay_cart():
    try:
        utils.pay_cart(cart=session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.route('/admin', methods=['post'])
def admin_login():
    err_msg = None
    try:
        if request.method.__eq__('POST'):
            username = request.form.get('username')
            password = request.form.get('password')

            user = utils.check_user_login(username=username, password=password, user_role=UserRole.ADMIN)
            if user:
                login_user(user=user)
            else:
                err_msg = 'Username or password is incorrect!'
    except Exception as ex:
        err_msg = str(ex)
    if err_msg:
        flash(err_msg)
    return redirect('/admin')


if __name__ == "__main__":
    from app.admin import *

    app.run(debug=True)
