import os
import telebot
import re


# =============================
# CONFIGURAÇÃO
# =============================
import os
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 798994990  # seu user_id do @userinfobot

# Palavras e padrões proibidos (para quem NÃO é você)
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

    # Qualquer mensagem de outro admin ou bot
    bot.delete_message(message.chat.id, message.message_id)

# =============================
# COMANDO DE TESTE (privado)
# =============================
@bot.message_handler(commands=['ping'])
def ping(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "🟢 Firewall ativo no canal.")

# =============================
bot.infinity_polling()
