from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = '56%^&*987^&*(098&*((*&^&*&'
app.config['SQLALCHEMY_DATABASE_URI'] = str.format('mysql+pymysql://root:{}@localhost/ecommerceapp?charset=utf8mb4',
                                                   'Omc6789#')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

app.config['PAGE_SIZE'] = 8

cloud_dict = {
    "cloud_name": "dad8ejn0r",
    "api_key": "916986197549325",
    "api_secret": "8ZDd8GQafg9rc9_h5UrIBt0SZ4Q"
}

cloudinary.config(
    cloud_name=cloud_dict["cloud_name"],
    api_key=cloud_dict["api_key"],
    api_secret=cloud_dict["api_secret"]
)

login = LoginManager(app=app)
