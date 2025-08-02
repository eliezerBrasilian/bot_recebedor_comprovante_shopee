import os

from telegram import BotCommand, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
from api.BotCuspidorApi import BotCuspidorAPI
from utils.utils import dividindo_mensagem

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

waiting_for_user_info = False

async def definir_menu(bot_app):
    comandos = [
        BotCommand("start", "📲 Iniciar bot"),
        BotCommand("informar_info", "Tornar usuário Premium")
    ]
    await bot_app.bot.set_my_commands(comandos)

async def informar_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for_user_info
    
    waiting_for_user_info = True
    await update.message.reply_text("Envie o ID do usuário e o ID do chat em que o usuário clicou em enviar_comprovante patar torná-lo premium\n\nNo formato: USER_ID-CHAT_ID-NOME\nExemplo: 123-456-João")
    
async def receber_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for_user_info
    
    if not waiting_for_user_info:
        return

    info_text = update.message.text
    
    user_id, chat_id, name = await dividindo_mensagem(update, info_text)
    
    api = BotCuspidorAPI()
     
    status = await api.tornar_premium(user_id)
    
    if status == 404:
        await api.criar_usuario(name=name, user_id_telegram=user_id)
        status = await api.tornar_premium(user_id)
    
    if status != 404:
        waiting_for_user_info = False

        response_message = f"Usuário {user_id} se tornou premium: \nResultado: {status == 201}"
        await update.message.reply_text(response_message)
        await enviar_para_canal_privado(context, user_id, chat_id, status)

    
async def enviar_para_canal_privado(context: ContextTypes.DEFAULT_TYPE, user_id, chat_id, status):
    CHAT_ID_DESTINO = -1002624250430
   
    await context.bot.send_message(
        chat_id=CHAT_ID_DESTINO,
        text="Encaminhando mensagem abaixo para o bot cuspidor responder ao usuário seu status de premium",
    )
   
    await context.bot.send_message(
        chat_id=CHAT_ID_DESTINO,
        text=f"{user_id}-{chat_id}-{status}",
        parse_mode="HTML"
    )


if BOT_TOKEN:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("informar_info", informar_info))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_info))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(definir_menu(app))
    app.run_polling()
