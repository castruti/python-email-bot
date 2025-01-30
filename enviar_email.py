import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
import config

# Função para enviar e-mail
def enviar_email(destinatario, assunto, corpo, anexo=None):
    msg = MIMEMultipart()
    msg['From'] = config.EMAIL
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # Corpo do e-mail
    msg.attach(MIMEText(corpo, 'plain'))

    # Anexo (se houver)
    if anexo:
        with open(anexo, 'rb') as arquivo:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(arquivo.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={anexo}')
            msg.attach(part)

    try:
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.EMAIL, config.PASSWORD)
            text = msg.as_string()
            server.sendmail(config.EMAIL, destinatario, text)
            print(f'E-mail enviado para {destinatario}')
    except Exception as e:
        print(f'Falha ao enviar e-mail para {destinatario}: {e}')

# Enviar para todos os destinatários no CSV
def enviar_para_lista():
    with open('emails.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            enviar_email(row['email'], config.SUBJECT, config.BODY)

# Chamada principal
if __name__ == "__main__":
    enviar_para_lista()
