from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las claves de las variables de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=OPENAI_API_KEY,  # This is the default and can be omitted
)

# Función para procesar mensajes
async def responder_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text

    print(mensaje_usuario)

    try:
        # Llamada a la API de OpenAI (usando Completion.create)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": mensaje_usuario,
                }
            ],
            model="gpt-4o",
        )

        print('Respuesta: ', chat_completion)

        # Respuesta del modelo
        texto_respuesta = chat_completion.choices[0].message.content
        await update.message.reply_text(texto_respuesta)
    except Exception as e:
        print(e)
        await update.message.reply_text("Lo siento, ocurrió un error procesando tu mensaje.")

# Configuración del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy un bot creado por Edu Oliva y mis respuestas se generan mediante IA. Envíame un mensaje y responderé.")

def main():
    # Inicializar la aplicación del bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Comandos y manejo de mensajes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensaje))

    # Iniciar el bot
    print("Bot en funcionamiento...")
    app.run_polling()

if __name__ == '__main__':
    main()
