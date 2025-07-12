
import os
import requests
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("أهلاً بك! أرسل IP أو بروكسي لفحصه.")

async def check_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
                results.append(f"[{service}]
{res.text}")
        except Exception as e:
            results.append(f"[{service}] Error: {e}")
    reply = "

".join(results) if results else "فشل الفحص."
    await update.message.reply_text(reply)

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_ip))
    app.run_polling()

if __name__ == "__main__":
    main()
    