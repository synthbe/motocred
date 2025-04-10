# googles.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError
from googleapiclient.errors import HttpError
from babel.numbers import format_currency
from datetime import datetime
import smtplib
import socket

from errors import AuthError, SheetError, EmailError
from type_aliases import Report, AnalysiResult, CustomerDataLoan, SheetBody

def extract_report(report: Report, status: AnalysiResult) -> SheetBody:
    data = report.get("reports", [{}])[0]

    name = data.get("registration", {}).get("consumerName", "NOME NÂO LOCALIZADO")
    status = status # Just to keep to order

    # Not really sure about negatives and debts
    debts = data.get("negativeData", 0).get("refin", 0).get("summary", 0).get("count", 0)
    debts_value = data.get("negativeData", 0).get("refin", 0).get("summary", 0).get("balance", 0.0)
    negativations = data.get("negativeData", 0).get("pefin", 0).get("summary", 0).get("count", 0)
    negativations_value = data.get("negativeData", 0).get("pefin", 0).get("summary", 0).get("balance", 0.0)

    score = data.get("score", {}).get("score", None)
    cpf_situation = data.get("registration", {}).get("statusRegistration", "SITUAÇÂO NÔA LOCALIZADA")
    birth_date = data.get("registration", {}).get("birthDate", "DATA DE NASCIMENTO NÃO LOCALIZADA")
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d").strftime("%d/%m/%Y") if birth_date != "DATA DE NASCIMENTO NÃO LOCALIZADA" else birth_date

    sheet_data = [[name, status, debts, debts_value, negativations, negativations_value, score, cpf_situation, birth_date]]

    return {"values": sheet_data}

def write_on_google_sheet(
    sheet_id: str,
    sheet_body: SheetBody,
) -> None:
    # Use Application Default Credentials (ADC)
    try:
        credentials, _ = default(scopes=["https://www.googleapis.com/auth/spreadsheets"])
    except DefaultCredentialsError:
        raise AuthError("Google Sheet Authentication Falied", 401)

    try:
        service = build("sheets", "v4", credentials=credentials)
        service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range="Sheet1!A2:J2",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=sheet_body
        ).execute()

    except HttpError as error:
        raise SheetError(f"An error occurred with Google Sheets API: {error}", 400)

    except Exception as error:
        raise SheetError(f"Unexpected error occurred: {error}", 500)

def create_copy(
    status: AnalysiResult | None=None,
    analysis_data: CustomerDataLoan | None=None,
    error: str | None=None,
) -> dict[str, str]:
    copy = dict()

    if error:
        subject = "Error"
        text = f"Hove um erro durante a análise serasa de uma venda. Verificar!! Error: {error}"
        copy["subject"] = subject
        copy["text"] = text

        return copy

    assert status != None
    assert analysis_data != None

    name = analysis_data.get("name", "Cliente")

    if "APROVADO" in status:
        # Creating copy of aprovação
        try:
            value_veic = analysis_data["value_veic"]
            value_fin = analysis_data["value_fin"]
            store = analysis_data["store"]
            parcs = analysis_data["parcs"]
        except KeyError as e:
            raise Exception(f"Error: {e}. During copy creation")

        parcs_text = (f"36x -> R$ {format_currency(parcs[2], 'BRL', locale='pt_BR')}\n"
                    f"24x -> R$ {format_currency(parcs[1], 'BRL', locale='pt_BR')}\n"
                    f"12x -> R$ {format_currency(parcs[0], 'BRL', locale='pt_BR')}\n")

        subject = "Parabéns, seu crédito foi aprovado!"
        text = (f"Parabéns, {name}!\n\n"
                f"Você foi pré aprovado para o crédito de {format_currency(value_fin, 'BRL', locale='pt_BR')} na moto de {format_currency(value_veic, 'BRL', locale='pt_BR')} da loja {store}.\n"
                "Você pode escolher os seguintes prazos:\n\n"
                f"{parcs_text} \n\n"
                "Informe ao vendedor o melhor prazo para você e seguiremos para a próxima etapa de análise. \n\n"
                "Obrigado!")

    elif "REPROVADO" in status:
        # Creating copy of reprovação
        subject = "Infelizmente seu crédito foi negado"
        text = (f"Olá, {name}. Infelizmente seu crédito foi negado.\n\n"
                "Você poderá realizar uma nova consulta em um prazo de 3 meses.\n\n"
                "Atenciosamente,\nEquipe Motocred")
    else:
        subject = "Análise de Crédito"
        text = "\nNossa equipe informa que ainda estamos fazendo a sua pré-análise, assim que possível entraremos em contato."

    copy["subject"] = subject
    copy["text"] = text

    return copy

def send_email(
    server: str,
    port: int,
    from_email: str,
    password: str,
    to_email: str,
    copy: dict[str, str]
) -> None:
    subject = copy["subject"]
    text = copy["text"]

    # Creating email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))

    # Sending e-mail
    try:
        with smtplib.SMTP(server, port, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(from_email, password)
            smtp.send_message(msg)

    except socket.timeout:
        raise EmailError(f"Connection timed out while sending email to {to_email}.", 504)

    except smtplib.SMTPAuthenticationError:
        raise AuthError("Email authentication failed. Invalid credentials", 404)

    except smtplib.SMTPConnectError:
        raise EmailError("Failed to connect to the email server", 503)

    except smtplib.SMTPRecipientsRefused:
        raise EmailError(f"Email {to_email} refused by the server", 400)

    except smtplib.SMTPException as e:
        raise EmailError(f"SMTP error occurred while sending email to {to_email}: {e}", 500)

    except Exception as e:
        raise RuntimeError(f"Unexpected error occurred while sending email to {to_email}: {e}", 500)
