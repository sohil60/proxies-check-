import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("أرسل عنوان IP لفحصه.")

async def check_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ip = update.message.text.strip()
    services = [
        "https://ipinfo.io/{ip}/json",
        "https://ip-api.com/json/{ip}",
        "https://ipx.ac/api/ip/{ip}",
    ]
    results = []

    for service in services:
        url = service.format(ip=ip)
        try:
            res = requests.get(url, timeout=5)
            if res.ok:
                results.append(f"[{service}] {res.text}")
            else:
                results.append(f"[{service}] خطأ بالرد.")
        except Exception as e:
            results.append(f"[{service}] Error: {e}")

    reply = "\n".join(results) if results else "فحص فشل"
    await update.message.reply_text(reply)

app = Application.builder().token("7246263388:AAHc3AkabjUHVjHxWxvjt3PJg7wWiW_drMA").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_ip))
app.run_polling()
