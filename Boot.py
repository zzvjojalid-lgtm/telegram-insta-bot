import os
import asyncio
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import subprocess

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط فيديو أو ريلز من إنستغرام 🎥")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        await update.message.reply_text("❌ أرسل رابط إنستغرام صحيح.")
        return

    msg = await update.message.reply_text("⏳ جاري التحميل ...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = ["yt-dlp", "-f", "mp4", "-o", f"{tmpdir}/video.%(ext)s", url]
            proc = await asyncio.create_subprocess_exec(*cmd)
            await proc.wait()

            video_path = f"{tmpdir}/video.mp4"
            await update.message.reply_video(video=open(video_path, "rb"))
            await msg.delete()
    except Exception as e:
        await msg.edit_text(f"حدث خطأ: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    app.run_polling()

if __name__ == "__main__":
    main()
