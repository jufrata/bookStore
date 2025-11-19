async function gerarPagamento() {
    const email = document.getElementById('email').value;
    const status = document.getElementById('status');

    if (!email) {
        status.innerText = "Digite um e-mail válido.";
        return;
    }

    status.innerText = "Gerando pagamento...";

    const response = await fetch("https://SEU-BACKEND.onrender.com/create-payment", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email })
    });

    const data = await response.json();

    document.getElementById("qrCode").src = data.qr_code_base64;
    document.getElementById("copiaCola").value = data.copia_cola;

    document.getElementById("pix-area").classList.remove("hidden");
    status.innerText = "";
}

async function confirmarPagamento() {
    const email = document.getElementById("email").value;
    const status = document.getElementById("status");

    status.innerText = "Verificando pagamento...";

    const response = await fetch("https://SEU-BACKEND.onrender.com/check-payment?email=" + email);

    const data = await response.json();

    if (data.pago) {
        status.innerText = "Pagamento confirmado! PDF enviado ao seu e-mail.";
    } else {
        status.innerText = "Pagamento ainda não localizado. Tente novamente em 30 segundos.";
    }
}
