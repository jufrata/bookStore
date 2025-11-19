from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import base64
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# --- CONFIG --- #
PDF_PATH = "livro.pdf"
PIX_CHAVE = os.getenv("PIX_CHAVE")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_SENHA = os.getenv("SMTP_SENHA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Banco de pagamentos simples em memória
payments = {}

@app.post("/create-payment")
def create_payment(data: dict):
    email = data["email"]

    # Simulação de QR Code e código copia e cola
    qr_fake = "QRCodeFake123"
    qr_base64 = base64.b64encode(qr_fake.encode()).decode()

    copia_cola = f"0002010102122688PIXCHAVE:{PIX_CHAVE}|EMAIL:{email}|VALOR:29.90"

    payments[email] = False  # Aguardando pagamento

    return {
        "qr_code_base64": "data:image/png;base64," + qr_base64,
        "copia_cola": copia_cola
    }


@app.get("/check-payment")
def check_payment(email: str):
    """
    Aqui você colocaria a consulta real à API do banco ou PSP.
    Para teste, vamos marcar manualmente em memória.
    """
    if email in payments and payments[email]:
        return {"pago": True}

    return {"pago": False}


@app.post("/confirm-manual")
def confirm_manual(data: dict):
    """Endpoint para você marcar manualmente como pago."""
    email = data["email"]
    payments[email] = True
    send_pdf(email)
    return {"ok": True}


def send_pdf(destinatario):
    msg = MIMEText("Segue em anexo seu livro digital!", "plain")
    msg["Subject"] = "Seu PDF"
    msg["From"] = SMTP_EMAIL
    msg["To"] = destinatario

    with open(PDF_PATH, "rb") as f:
        pdf_bytes = f.read()

    # Se quiser enviar o PDF como anexo, posso adicionar o código depois

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SMTP_EMAIL, SMTP_SENHA)
    server.sendmail(SMTP_EMAIL, destinatario, msg.as_string())
    server.quit()
