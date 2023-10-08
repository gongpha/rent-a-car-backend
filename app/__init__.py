""" สร้าง Flask App ขึ้นมา และกำหนดค่าต่าง ๆ ที่จำเป็น """
import os
import secrets
from flask import Flask, redirect
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from dotenv import load_dotenv
from oauthlib.oauth2 import WebApplicationClient

from datetime import timedelta

# modules
from app.playground import bp as playground_bp
from app.auth import bp as auth_bp
from app.booking import bp as booking_bp
from app.customer import bp as customer_bp
from app.cars import bp as cars_bp
from app.reservations import bp as reservations_bp

from .utils.database import init_db

from flask_jwt_extended import JWTManager

load_dotenv()

client = WebApplicationClient(os.getenv("GOOGLE_CLIENT_ID"))

# sql = SQLAlchemy () <- will uncomment this if anybody want to use ORM stuff

def init_app() -> Flask :
    """ initialize the flask app """
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config["JWT_COOKIE_SECURE"] = os.getenv("COOKIE_SECURE", True)
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_SECRET_KEY"] = secrets.token_bytes(16) # os.urandom(16)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    app.config["JWT_COOKIE_SAMESITE"] = "None"

    app.jwt = JWTManager(app)

    # login system

    # ตั้งค่าให้เชื่อมกับฐานข้อมูล
    # ค่าทั้งหมดอยู่ในไฟล์ .env ของ Server ; อย่าปล่อยให้หลุดออกมาเด็ดขาด !
    app.config['MYSQL_DATABASE_HOST'] = os.getenv("DATABASE_HOST")
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv("DATABASE_PORT"))
    app.config['MYSQL_DATABASE_USER'] = os.getenv("DATABASE_USER")
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DATABASE_PASSWORD")
    app.config['MYSQL_DATABASE_DB'] = os.getenv("DATABASE_DATABASE")
    init_db(app)

    app.client = client

    # register blueprint ต่าง ๆ
    app.register_blueprint(auth_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(cars_bp)
    app.register_blueprint(reservations_bp)
    
    app.register_blueprint(playground_bp)

    # สร้าง route สำหรับ redirect ไปยังหน้าเว็บหลัก
    # กรณีที่มีคนเข้ามาที่หน้า / ของ Server โดยตรง (อย่าหาทำ)
    @app.route("/")
    def home() :
        return redirect("https://rentacar.iservkmitl.tech/", code=302)

    return app