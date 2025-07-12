
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل عنوان IP لفحصه.")

async def check_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip = update.message.text.strip()
    results = []
    for service in [
        f"https://ipinfo.io/{ip}/json",
        f"https://ip-api.com/json/{ip}",
        f"https://ipx.ac/api/ip/{ip}",
    ]:
        try:
            res = requests.get(service, timeout=5)
            if res.ok:
                results.append(f"[{service}] {res.text}")
            else:
                results.append(f"[{service}] Request failed with status code {res.status_code}")
        except Exception as e:
            results.append(f"[{service}] Error: {str(e)}")
    reply = "\n\n".join(results) if results else "الفحص فشل."
    await update.message.reply_text(reply)
def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_ip))
    app.run_polling()

if __name__ == "__main__":
    main()
