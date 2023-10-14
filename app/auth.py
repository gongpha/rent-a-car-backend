""" auth """
from flask import Blueprint
import requests
import os
import json
from flask import redirect, request, current_app, jsonify
from datetime import datetime, timezone, timedelta
from functools import wraps
from app.utils.database import execute_sql_one

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies, get_jwt,

    verify_jwt_in_request
)

from app.models.account import Account

bp = Blueprint('auth', __name__)

# @bp.route("/oauth2/authorize", methods=["GET"])
# def authorize() :
#     """ authorize oauth2 """

# @bp.route("/oauth2/token", methods=["GET"])
# def token() :
#     """ token oauth2 """

# GOOGLE LOGIN #

def get_google_provider_cfg() :
    return requests.get("https://accounts.google.com/.well-known/openid-configuration").json()

@bp.route("/googlelogin/auth")
def google_login_auth() :
    """ send me bacc a code """
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    client = current_app.client

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url="postmessage",
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(os.getenv("GOOGLE_CLIENT_ID"), os.getenv("GOOGLE_CLIENT_SECRET")),
    )
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    userdata = userinfo_response.json()

    if not userdata.get("email_verified") :
        return {
            "return": "ERROR",
            "error": "User email not available or not verified by Google."
        }, 400

    acc = Account.get_by_email(userdata["email"])
    if not acc :
        # owo new account
        Account.create_with_customer(
            userdata["given_name"],
            userdata["family_name"],
            userdata["email"],
            None,
            None,
            userdata["picture"]
        )
        returnstr = ("ACCOUNT_CREATED", 201)
    else :
        # owo existing account
        returnstr = ("ACCOUNT_EXISTS", 200)

    # login
    # imma make a token
    token = create_access_token(
        identity=userdata["email"], additional_claims={
            "type" : "user",
            "role" : "customer"
        }
    )

    # go bacc
    resp = jsonify({
        "return" : returnstr[0]
    })
    set_access_cookies(resp, token) # heres the token
    return resp, returnstr[1]

@bp.route("/logout", methods=["POST"])
def logout() :
    response = jsonify({"return": "LOGGED_OUT"})
    unset_jwt_cookies(response) # goodbye token
    return response

def user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["type"] == "user" :
                return fn(*args, **kwargs)
            else:
                response = jsonify({
                    "return" : "ERROR",
                    "error" : "User-only endpoint"
                })
                return response, 403

        return decorator

    return wrapper

# @bp.after_request
# def refresh_jwt(response) :
#     # in case if the token is about to expire
#     try :
#         target_timestamp = datetime.timestamp(
#             datetime.now(timezone.utc) + timedelta(hours=1)
#         )
#         if target_timestamp > get_jwt()["exp"] :
#             # expired. refresh
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError) :
#         # wow nothing to refresh
#         return response

#################

@bp.route("/profile/button", methods=["GET"])
@user_required()
def profile_button() :
    """ profile button """
    acc = Account.get_by_email(get_jwt_identity())
    if not acc :
        return {
            "return" : "ERROR",
            "error" : "Account not found."
        }, 404

    return {
        "return" : "OK",
        "acc_id" : acc.id,
        "displayname" : acc.display_name,
        "email" : acc.customer.email,
        "first_name" : acc.customer.first_name,
        "last_name" : acc.customer.last_name,
        "phone" : acc.customer.phone,
        "picture" : acc.pfp_url
    }

#################
# ADMIN

import hashlib
from .models.accountemp import AccountEmp

@bp.route("/admin/login", methods=["POST"])
def admin_login() :
    """ admin login """
    json_data = request.get_json(force=True)
    username = json_data.get("username")
    password = json_data.get("password")

    if not username or not password :
        return {
            "return" : "ERROR",
            "error" : "Missing username or password."
        }, 400

    password_md5 = hashlib.md5(password.encode()).hexdigest()

    acc = AccountEmp.get_by_username(username)

    # fixme : merge with the below ?
    if not acc :
        return {
            "return" : "ERROR",
            "error" : "Account not found."
        }, 404
    if acc.password_md5 != password_md5 :
        return {
            "return" : "ERROR",
            "error" : "Incorrect password."
        }, 401

    # yee
    token = create_access_token(identity=username, additional_claims={
        "type" : "admin",
        "role" : acc.employee.role
    })

    resp = jsonify({
        "return" : "GRANTED"
    })
    set_access_cookies(resp, token, )
    return resp, 200

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["type"] == "admin":
                return fn(*args, **kwargs)
            else:
                response = jsonify({
                    "return" : "ERROR",
                    "error" : "Admin-only endpoint"
                })
                return response, 403

        return decorator

    return wrapper

def manager_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["type"] == "admin":
                if claims["role"] == "MANAGER" :
                    return fn(*args, **kwargs)
            response = jsonify({
                "return" : "ERROR",
                "error" : "Manager-only endpoint"
            })
            return response, 403

        return decorator

    return wrapper

def root_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["type"] == "admin":
                if claims["role"] == "ROOT" :
                    return fn(*args, **kwargs)
            response = jsonify({
                "return" : "ERROR",
                "error" : "Root-only endpoint"
            })
            return response, 403

        return decorator

    return wrapper

@bp.route("/admin/me", methods=["GET"])
@admin_required()
def admin_me() :
    """ admin me """

    acc = execute_sql_one(
        "SELECT username, e_first_name, e_last_name, name FROM employees"
        " JOIN web_accounts_emp USING (employee_id)"
        " JOIN branches USING (branch_id)"
        " WHERE username = %s"
        , get_jwt_identity()
    )

    if not acc :
        return {
            "return" : "ERROR",
            "error" : "Account not found."
        }, 404

    return {
        "return" : "OK",
        
        "username" : acc[0],
        "first_name" : acc[1],
        "last_name" : acc[2],
        "branch_name" : acc[3]
    }