""" auth """
from flask import Blueprint
import requests
import os
import json
from flask import redirect, request, current_app, jsonify
from datetime import datetime, timezone, timedelta

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    set_access_cookies, unset_jwt_cookies, get_jwt
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
    token = create_access_token(identity=userdata["email"])

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
@jwt_required()
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
        
        "displayname" : acc.display_name,
        "picture" : acc.pfp_url
    }