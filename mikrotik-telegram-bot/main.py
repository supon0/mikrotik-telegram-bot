from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN, MIKROTIK_CONFIG
from librouteros import connect

def connect_mikrotik():
    return connect(
        host=MIKROTIK_CONFIG['host'],
        username=MIKROTIK_CONFIG['username'],
        password=MIKROTIK_CONFIG['password'],
        port=MIKROTIK_CONFIG['port']
    )
async def traffic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        api = connect_mikrotik()
        interfaces = api.path("interface").get()
        response = ""
        for iface in interfaces:
            name = iface['name']
            rx = iface.get('rx-byte', '0')
            tx = iface.get('tx-byte', '0')
            response += f"{name}: RX={rx}, TX={tx}\n"
        await update.message.reply_text(response or "Tidak ada data.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        api = connect_mikrotik()
        api.path("system", "reboot").call("=", {})
        await update.message.reply_text("MikroTik sedang direboot...")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
      
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot siap! Ketik /ip untuk lihat IP address MikroTik.")

async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        api = connect_mikrotik()
        ip_list = api.path("ip", "address").get()
        message = "\n".join([f"{ip['address']} on {ip['interface']}" for ip in ip_list])
        await update.message.reply_text(f"IP MikroTik:\n{message}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ip", ip))
    app.add_handler(CommandHandler("reboot", reboot))
    app.add_handler(CommandHandler("traffic", traffic))
    app.run_polling()
