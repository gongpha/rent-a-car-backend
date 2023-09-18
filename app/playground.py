""" ไฟล์นี้ จะลองทำอะไรก็ได้ """

from flask import Blueprint

bp = Blueprint('playground', __name__)

@bp.route("/test", methods=["GET"])
def test() :
    """ test """
    return "test test 123"

@bp.route("/bruh", methods=["GET"])
def bruh() :
    """ ปล่อย JSON ออกไปว่า bruh """
    return {"message" : "bruh"}
