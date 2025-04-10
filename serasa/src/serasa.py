# serasa.py
import requests
import base64

from errors import CPFError, AuthError, ReportError
from type_aliases import Report, AnalysiResult

def get_basic_iam(client_id: str, cliend_sercret: str) -> str:
    credentials = f"{client_id}:{cliend_sercret}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()

    return b64_credentials

def get_auth(url: str, encoded_credential: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credential}",
    }

    response = requests.post(url=url, headers=headers, json={})

    if response.status_code >= 200 and response.status_code < 300:
        token = response.json().get("accessToken")
        if token:
            return token
        else:
            raise AuthError("Token not found in response", 504)
    else:
        raise AuthError(response.text, response.status_code)

def get_report(url: str, cpf: str, token: str) -> Report:
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Document-id": cpf,
    }

    response = requests.get(url=url, headers=headers, json={})

    if response.status_code == 200:
        try:
            return response.json()
        except:
            raise ReportError()

    if response.status_code == 404:
        raise CPFError("CPF not found or invalid")
    else:
        raise Exception(f"Request failed! Status: {response.status_code}\nResponse: {response.text}")

def pre_analysi(report: Report) -> AnalysiResult:
    # Pode nao calcular o score
    data = report.get('reports', [{}])[0]
    score = data.get('score', {}).get('score', None)
    negativations = data.get('negativeData', {}).get('pefin', {}).get('summary', {}).get('count', 0)
    negativations_value = data.get('negativeData', {}).get('pefin', {}).get('summary', {}).get('balance', 0.0)
    debts = data.get('negativeData', {}).get('refin', {}).get('summary', {}).get('count', 0)
    debts_value = data.get('negativeData', {}).get('refin', {}).get('summary', {}).get('balance', 0.0)

    if not score:
        return "SCORE NÂO CALULADO"

    if int(score) < 200:
        return "REPROVADO POR SCORE"
    elif int(negativations + debts) > 5:
        return "REPROVADO POR QUANTIDADE DE NEGATIVACOES E DIVIDAS"
    elif float(negativations_value + debts_value) > 3000:
        return "REPROVADO POR VALOR DAS NEGATIVACOES E DIVIDAS"
    else:
        return "PRE APROVADO"

def calculate_fin(
    value_veic: float,
    value_in: float,
    report: Report,
    cred_lim: float=12000.00
) -> tuple[float, tuple[float, float, float]]:
    data = report.get('reports', [{}])[0]
    score = data.get('score', {}).get('score', None)

    if value_in > value_veic: # Assuming that the these forms field were switeched when filled
        value_veic, value_in = value_in, value_veic

    p_in = 0.5 if score < 450 else 0.4
    value_fin = value_veic - value_in
    if value_in < value_veic * p_in:
        value_fin = value_veic * p_in
    value_fin = value_t = min(cred_lim, value_fin)

    if value_fin <= 5000:
        value_t += 700
    elif value_fin > 5000 and value_fin <= 7000:
        value_t += 820
    elif value_fin > 7000 and value_fin <= 10000:
        value_t += 870
    elif value_fin > 10000:
        value_t += 920

    parc_12 = (value_t * 1.48) / 12
    parc_24 = (value_t * 1.96) / 24
    parc_36 = (value_t * 2.44) / 36

    return value_fin, (parc_12, parc_24, parc_36)
