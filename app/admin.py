from app import app, db, utils
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import Category, Product, User, Receipt, ReceiptDetail, UserRole
from flask_login import current_user, logout_user
from flask import redirect


class AuthenticationView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyCategoryView(AuthenticationView):
    column_list = ['name', 'products']


class MyProductView(AuthenticationView):
    column_list = ['name', 'price', 'category']


class MyUserView(AuthenticationView):
    column_list = ['full_name', 'email', 'username', 'joined_date', 'user_role']


class MyReceiptView(AuthenticationView):
    column_list = ['created_date', 'user', 'receipt_details']


class StatusView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/status.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutAdminView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', cate_stats=utils.category_stats())


admin = Admin(app=app,
              name='E-commerce Administration',
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyUserView(User, db.session))
admin.add_view(MyReceiptView(Receipt, db.session))
admin.add_view(AuthenticationView(ReceiptDetail, db.session))
admin.add_view(StatusView(name='Report'))
admin.add_view(LogoutAdminView(name='Sign out'))
