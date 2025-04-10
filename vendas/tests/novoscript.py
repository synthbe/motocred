import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# armazenamento@armazenamento-de-dados-serasa.iam.gserviceaccount.com

# AKfycbz0AvAYYQtbdWcXfVYAYCEf3c6TCAMN08FJeCsX6GwhjVrngF4goJsC5zwKgmEhhIVTOQ

# https://script.google.com/a/macros/motocred.digital/s/AKfycbz0AvAYYQtbdWcXfVYAYCEf3c6TCAMN08FJeCsX6GwhjVrngF4goJsC5zwKgmEhhIVTOQ/exec

#xhost +

planilha = 'https://docs.google.com/spreadsheets/d/1DpQic6P2porRZdLKeLEBct6aZisbAQ2h346yBVRMP9A/export?format=csv'

df = pd.read_csv(planilha)

loja = str(df.iloc[-1, 3])
nome = str(df.iloc[-1, 1])
cpf = str(df.iloc[-1, 7])
email = str(df.iloc[-1, 9])
cel = str(df.iloc[-1, 10])
renda = str(df.iloc[-1, 11]) + "00"
cnh = str(df.iloc[-1, 8])
valorveiculo = str(df.iloc[-1, 5]) + "0"
entrada = str(df.iloc[-1, 6])

if loja.lower() == 'carbumotos':
    user = "gabrielpdantas96@gmail.com"
    senha = "@Gd36119698"
elif loja.lower() == 'fina motos' or loja.lower() == "finamotos":
    user = "erika.callina@gmail.com"
    senha = "@Talu0511"
elif loja.lower() == 'brasilmotos' or loja.lower() == "brasil motos":
    user = "brasilmotos_kriss@hotmail.com"
    senha = "vendedor"
elif loja.lower() == 'rnmotos' or loja.lower() == "rn motos":
    user = "rnmotos_@hotmail.com"
    senha = "hb3s2qgp"
elif loja.lower() == 'motocerta' or loja.lower() == "motocerta":
    user = "alyssonrafaelt01@gmail.com"
    senha = "vendedor"
else:
    user = "junior@motocred.digital"
    senha = "Jan1&akKla01&98*am"

#CADASTRO DE USUÁRIO

driver = webdriver.Chrome()
driver.maximize_window()

driver.get('https://auto.altisapp.com/login')


username_field = driver.find_element(By.ID, 'email')
password_field = driver.find_element(By.ID, 'password')


username_field.send_keys(user)
password_field.send_keys(senha)


pyautogui.press('enter')

time.sleep(2)

clientes_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/nav/div/div[3]/button[2]')
clientes_btn.click()

time.sleep(2)

pyautogui.press('tab', presses=5)
pyautogui.press('enter')

time.sleep(1)

nome_input = driver.find_element(By.ID, 'name')
nome_input.send_keys(nome)

cpf_input = driver.find_element(By.ID, 'document')
cpf_input.send_keys(cpf)

email_input = driver.find_element(By.ID, 'email')
email_input.send_keys(email)

cel_input = driver.find_element(By.ID, 'phone')
cel_input.send_keys(cel)

renda_input = driver.find_element(By.ID, 'income')
renda_input.send_keys(renda)

menu = driver.find_element(By.XPATH, '/html/body/div[3]/form/div[7]/button')
menu.click()

pyautogui.press('space')

pyautogui.press('tab')
pyautogui.press('enter')

#CALCULO DE PARCELAS

time.sleep(2)

simulacao_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/nav/div/div[3]/div/button')

time.sleep(1)

simulacao_button.click()

time.sleep(1)

menu_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/button')

time.sleep(1)

menu_button.click()

pyautogui.press('enter')

time.sleep(1)

tipoveiculo_button = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div[3]/form/div/div[1]/div/div[2]/div[1]/div/button')

time.sleep(1)

tipoveiculo_button.click()

time.sleep(1)

novousado_button = driver.find_element(By.XPATH, '//*[@id="pre-owned"]')

novousado_button.click()

time.sleep(0.5)

marcaveiculo_button = driver.find_element(By.XPATH, '//*[@id=":r22:-form-item"]')

marcaveiculo_button.click()

pyautogui.typewrite("HONDA")

time.sleep(1)
pyautogui.press('enter')
pyautogui.press("tab")
pyautogui.press("tab")
pyautogui.press('enter')
time.sleep(0.5)
pyautogui.typewrite("biz")
time.sleep(3)
pyautogui.press('enter')
time.sleep(0.5)
pyautogui.press('tab')
time.sleep(0.5)
pyautogui.press("enter")
time.sleep(0.5)
pyautogui.press("enter")
time.sleep(0.5)
pyautogui.press("tab")
time.sleep(0.5)
pyautogui.press("enter")
time.sleep(0.5)
pyautogui.press("enter")
time.sleep(5)
pyautogui.press("tab")
time.sleep(1)
pyautogui.typewrite(valorveiculo)
pyautogui.press("tab")
time.sleep(1)
pyautogui.press("enter")
time.sleep(1)

#MESA DE CRÉDITO

user = "junior@motocred.digital"
senha = "Jan1&akKla01&98*am"

driver.get('https://credit-engine.altisapp.com/policies')

username_field = driver.find_element(By.ID, 'email')
password_field = driver.find_element(By.ID, 'password')

username_field.send_keys(user)
password_field.send_keys(senha)

pyautogui.press('enter')
time.sleep(2)

consultas_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/nav/button[3]')

time.sleep(3)

consultas_button.click()

time.sleep(5)

pyautogui.press("tab", presses=7)
pyautogui.press("enter", presses=2)
time.sleep(1.2)
pyautogui.press("tab")
pyautogui.press("enter")

time.sleep(1)

#RETORNO DO RESULTADO

elemento = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/h3/button/div/div")
texto = elemento.text.strip()
#############
elemento = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[4]")
dividas = elemento.text.strip()

elemento = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[2]/td[4]")
vldividas = elemento.text.strip()

elemento = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[3]/td[4]")
negativacoes = elemento.text.strip()

elemento = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[4]/td[4]")
vlnegativacoes = elemento.text.strip()

elemento = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[5]/td[4]")
score = elemento.text.strip()

elemento = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[6]/td[4]")
situaccpf = elemento.text.strip()

elemento = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div/div/div/table/tbody/tr[7]/td[4]")
idade = elemento.text.strip()

print(dividas, vldividas, negativacoes, vlnegativacoes, score, situaccpf, idade)

if int(score) < 200:
    resultado = "REPROVADO POR SCORE"
elif int(negativacoes) > 5:
    resultado = "REPROVADO POR QUANTIDADE DE NEGATIVACOES"
elif float(vlnegativacoes) > 3000:
    resultado = "REPROVADO POR VALOR DAS NEGATIVACOES"
else:
    resultado = "PRE APROVADO"


if int(score) > 500:
    porcentagem_entrada = 0.4
else:
    porcentagem_entrada = 0.5


valor_financiado = float(valorveiculo) - float(entrada)
if valor_financiado > 12000:
    valor_financiado = 12000

def calcular_parcela():
    valor = valor_financiado
    if valor <= 5000:
        valor_total = valor + 770
    elif valor > 5000 and valor <= 7000:
        valor_total = valor + 820
    elif valor > 7000 and valor <= 10000:
        valor_total = valor + 870
    elif valor > 10000:
        valor_total = valor + 920

    parcela_12 = (valor_total * 1.48) / 12
    parcela_24 = (valor_total * 1.96) / 24
    parcela_36 = (valor_total * 2.44) / 36

    result_text = (f"36x -> R$ {parcela_36:.2f}\n"
                    f"24x -> R$ {parcela_24:.2f}\n"
                    f"12x -> R$ {parcela_12:.2f}")

    return result_text

parcelas = calcular_parcela()
#preenchimento da planilha serasa


time.sleep(2)

ficha = (f"DIVIDAS -> {dividas}\n"
         f"VALOR DAS DÍVIDAS -> {vldividas}\n"
         f"NEGATIVACOES -> {negativacoes}\n"
         f"VALOR DAS NEGATIVACOES -> {vlnegativacoes}\n"
         f"SCORE -> {score}\n"
         f"SITUACAO DO CPF -> {situaccpf}\n"
         f"IDADE -> {idade}")

subprocess.Popen(["google-chrome", "--new-window", "https://app.slack.com/client/T07B8AEKLNN/C082BMW2858"])
time.sleep(15)
pyautogui.typewrite(nome + " - " + resultado.upper() + "\n\n" + ficha + "\n\n" + parcelas)
pyautogui.press("enter")

# Configurar o servidor SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
meu_email = "contato@motocred.digital"
minha_senha = "covb okjy jaiw imqo"

def calcular_valor_maximo(renda):
    parcela_maxima = renda / 3
    taxas = [(5000, 770), (7000, 820), (10000, 870), (float('inf'), 920)]
    for limite, taxa in taxas:
        valor = (parcela_maxima * 36 / 2.44) - taxa
        if valor <= limite:
            return max(valor, 0)
    return 0

renda = float(df.iloc[-1, 11])

if resultado.upper() == "PRE APROVADO":
    assunto = "Parabéns, seu crédito foi aprovado!"
    corpo = (f"Parabéns, {nome}!\n\n"
         f"Você foi pré aprovado para o crédito de R$ {valor_financiado} na moto de R$ {valorveiculo} da {loja}.\n"
         "Você pode escolher os seguintes prazos:\n\n"
         f"{parcelas}. \n\n"
         "Informe ao vendedor o melhor prazo para você e seguiremos para a próxima etapa da análise.\n\n"
         "Obrigado!")

else:
    assunto = "Infelizmente seu crédito foi negado"
    corpo = (f"Olá, {nome}. Infelizmente seu crédito foi negado.\n\n"
            "Você poderá realizar uma nova consulta em um prazo de 3 meses.\n\n"
            "Atenciosamente,\nEquipe Motocred")



# Criar a mensagem de e-mail
msg = MIMEMultipart()
msg['From'] = meu_email
msg['To'] = email
msg['Subject'] = assunto
msg.attach(MIMEText(corpo, 'plain'))

# Enviar o e-mail
try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(meu_email, minha_senha)
        server.send_message(msg)
        print("E-mail enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar o e-mail: {e}")







ano_nascimento = datetime.now().year - int(idade)
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Escopos necessários para acessar e modificar planilhas
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# ID da planilha e intervalo de células onde os dados serão adicionados
SPREADSHEET_ID = '11KlDHqlwom_zNN5Xvfom-8dXVZTCy75mWHbep5NqfRY'  # ID da sua planilha
RANGE_NAME = 'Sheet1!A2:A'  # Intervalo começando abaixo do cabeçalho

def main():
    creds = None

    # Verifica se há um token salvo de sessão anterior
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Se não houver credenciais válidas, inicia o fluxo de autenticação
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/rodrigo/Área de Trabalho/Automacao/api/client_secret_56520928112-4tp55n3f5o6glapjj6ddvh4h4tsd2vge.apps.googleusercontent.com.json', SCOPES
            )  # Caminho do arquivo de credenciais OAuth
            creds = flow.run_local_server(port=0)

        # Salva as credenciais para reutilização futura
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Cria o serviço do Google Sheets
    service = build('sheets', 'v4', credentials=creds)

    # Dados organizados para envio à planilha
    values = [[nome, resultado, dividas, vldividas, negativacoes, vlnegativacoes, score, situaccpf, ano_nascimento]]
    body = {
        'values': values
    }

    # Adiciona os dados à planilha sem sobrescrever os existentes
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',  # Dados serão inseridos como texto bruto
        insertDataOption='INSERT_ROWS',  # Adiciona uma nova linha
        body=body
    ).execute()

    print(f"{result.get('updates').get('updatedCells')} células foram adicionadas.")

if __name__ == '__main__':
    main()
