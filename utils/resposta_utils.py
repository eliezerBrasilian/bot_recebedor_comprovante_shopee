from telegram import Update

async def responder_usuario(update: Update, texto: str, **kwargs):
    if update.message:
        await update.message.reply_text(texto, **kwargs)
    elif update.callback_query:
        await update.callback_query.edit_message_text(texto, **kwargs)

async def enviar_video_ao_usuario(update: Update, video: bytes, **kwargs):
    if update.message:
        await update.message.reply_video(video=video, **kwargs)
    elif update.callback_query:
        await update.callback_query.message.reply_video(video=video, **kwargs)
        
async def enviar_foto_ao_usuario(update: Update, foto: bytes, **kwargs):
    if update.message:
        await update.message.reply_photo(photo=foto, **kwargs)
    elif update.callback_query:
        await update.callback_query.message.reply_photo(photo=foto, **kwargs)
