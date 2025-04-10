# main.py
from flask import Request, Response, jsonify
from dotenv import load_dotenv
import logging
import functions_framework
import os

from serasa import get_auth, get_basic_iam, get_report, pre_analysi, calculate_fin
from googles import write_on_google_sheet, send_email, extract_report, create_copy
from errors import RequestError

load_dotenv()

# Serasa
SERASA_CLIENT_ID = os.getenv("SERASA_CLIENT_ID")
SERASA_CLIENT_SECRET = os.getenv("SERASA_CLIENT_SECRET")
AUTH_URL = os.getenv("AUTH_URL")
REQ_URL = os.getenv("REQUEST_URL")

# Google Sheets
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
PROJECT_ID = os.getenv("PROJECT_ID")
AUTH_URI = os.getenv("AUTH_URI")
TOKEN_URI = os.getenv("TOKEN_URI")
AUTH_PROVIDER_X509_CERT_URL = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Email
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")


@functions_framework.http
def main(request: Request) -> tuple[Response, int]:
    try:
        request_json = request.get_json(silent=True) or {}
        if 'cpf' not in request_json:
            raise RequestError("No cpf key found in received request")
        if 'email' not in request_json:
            raise RequestError("No email key found in the received request")
        if 'name' not in request_json:
            raise RequestError("No name key found in the received request")
        if 'store' not in request_json:
            raise RequestError("No store key found in the received request")
        if 'valueVeic' not in request_json:
            raise RequestError("No value_veic key found in the received request")
        if 'valueIn' not in request_json:
            raise RequestError("No value_in key found in the received request")
        if 'renda' not in request_json:
            raise RequestError("No renda key found in the received request")

        # ------------------------------------------- Serasa request part --------------------------------------

        cpf = request_json["cpf"]
        email = request_json["email"]
        name = request_json["name"]
        store = request_json["store"]
        value_veic = request_json["valueVeic"]
        value_in = request_json["valueIn"]
        renda = request_json["renda"]

        if not SERASA_CLIENT_ID or not SERASA_CLIENT_SECRET or not AUTH_URL or not REQ_URL:
            raise ValueError("One or more values required for Serasa API could not be loaded")

        logging.info("Starting Serasa API request")

        credential = get_basic_iam(SERASA_CLIENT_ID, SERASA_CLIENT_SECRET)
        token = get_auth(AUTH_URL, credential)

        report = get_report(REQ_URL, cpf, token)
        status_client = pre_analysi(report)

        if value_in > value_veic: # Assuming that the these forms field were switeched when filled
            value_veic, value_in = value_in, value_veic

        logging.info("Calculating loan")
        value_fin, parcs = calculate_fin(float(value_veic), float(value_in), report)

        # ------------------------------------- Google Sheets part -----------------------------------------

        if not GOOGLE_SHEET_ID:
            raise ValueError("Google sheet id could not be loaded")

        logging.info("Writing into google sheets")

        body = extract_report(report, status_client)
        body["values"][0].append(renda)

        write_on_google_sheet(GOOGLE_SHEET_ID, body)

        # ----------------------------------- Email part -------------------------------------------

        if not SMTP_SERVER or not SMTP_PORT or not EMAIL or not EMAIL_PASSWORD:
            raise ValueError("One or more values required for email could not be loaded")

        logging.info("Sending email")
        email = EMAIL # TESTIN, TAKE THIS OFF WHEN IN FULLY PRODUCTION

        analysis_data = {"name": name, "value_veic": value_veic, "value_fin": value_fin, "parcs": parcs, "store": store}
        copy = create_copy(status=status_client, analysis_data=analysis_data,)

        send_email(SMTP_SERVER, SMTP_PORT, EMAIL, EMAIL_PASSWORD, email, copy)

        logging.info(f"Email sent to {email} with status {status_client}")
        return jsonify({"message": "Success", "status": status_client}), 200

    except Exception as e:
        logging.info(f"Unexpected error: {e}")

        copy = create_copy(error=str(e))
        send_email(SMTP_SERVER, SMTP_PORT, EMAIL, EMAIL_PASSWORD, EMAIL, copy)

        status_code = getattr(e, "status_code", 500)
        return jsonify({"error": str(e)}), status_code
