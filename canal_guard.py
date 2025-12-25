import os
import telebot
import re
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# =============================
# CONFIGURAÇÃO
# =============================
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 798994990  # seu user_id do @userinfobot

BLOCK = r"(http|https|www\.|\.com|\.br|t\.me|wa\.me|pix|r\$|usd|dólar|real|promo|oferta|venda)"

bot = telebot.TeleBot(TOKEN)

print("🔥 Clã Watanabe Bot Firewall ATIVO")

# =============================
# PROTEÇÃO DO CANAL
# =============================
@bot.channel_post_handler(func=lambda m: True)
def protect_channel(message):
    text = message.text or ""
    user = message.from_user

    # Postagem automática do próprio bot
    if user is None:
        return

    # Dono pode postar qualquer coisa
    if user.id == OWNER_ID:
        return

    # Qualquer outro → apaga
    if re.search(BLOCK, text.lower()):
        bot.delete_message(message.chat.id, message.message_id)
        return

    # Qualquer outra mensagem também é apagada
    bot.delete_message(message.chat.id, message.message_id)

# =============================
# COMANDO DE TESTE (privado)
# =============================
@bot.message_handler(commands=['ping'])
def ping(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "🟢 Firewall ativo no canal.")

# =============================
# SERVIDOR HTTP FALSO (Koyeb)
# =============================
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_http():
    server = HTTPServer(("0.0.0.0", 8000), DummyHandler)
    print("HTTP server running on 8000")
    server.serve_forever()

# =============================
# START
# =============================
def main():
    # sobe servidor HTTP primeiro
    threading.Thread(target=run_http, daemon=True).start()

    # dá tempo pro Koyeb enxergar a porta
    time.sleep(2)

    # inicia o bot
    print("Starting Telegram bot")
    bot.infinity_polling(skip_pending=True)

main()
