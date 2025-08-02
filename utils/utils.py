from telegram import Update

async def dividindo_mensagem(update:Update, info_text:str):
    partes = info_text.strip().split('-', 2)  # no máximo 3 partes
    if len(partes) < 3:
        await update.message.reply_text(
            "Formato inválido! Use: USER_ID-CHAT_ID-NOME\nExemplo: 123-456-João"
        )
        return
    return partes
