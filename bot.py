import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Configuration
BOT_TOKEN = "7684211673:AAFsw84HPEdZP42JrcHh_vsiq89EUmf3VVo"  # 🔒 TESTING ONLY - REVOKE LATER!
CHANNEL_LINK = "https://t.me/your_channel"  # Replace with your channel
GROUP_LINK = "https://t.me/your_group"      # Replace with your group
TWITTER_LINK = "https://twitter.com/your_twitter"  # Replace with your Twitter

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("✅ Done", callback_data="submit_wallet")]
    ]
    
    await update.message.reply_text(
        "📢 *AIRDROP BOT\n\n"
        "To qualify for 10 SOL airdrop:\n"
        "1. Join our channel\n"
        "2. Join our group\n"
        "3. Follow our Twitter\n\n"
        "Click ✅ Done after completing all steps*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_wallet_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This will trigger on ANY text message after clicking "Done"
    await update.message.reply_text(
        "🎉 *Congratulations! 10 SOL is on its way to your wallet!\n\n"
        "Transaction will appear in your wallet within 24 hours.*",
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "submit_wallet":
        await query.edit_message_text("📥 *Send your Solana wallet address:*\n\n(e.g., `5Hw...` or `https://solscan.io/account/...`)", 
                                     parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet_submission))
    
    # Render deployment setup
    port = int(os.environ.get("PORT", 8443))
    webhook_url = os.environ.get("RENDER_EXTERNAL_URL")
    
    if webhook_url:
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=f"{webhook_url}/webhook"
        )
    else:
        app.run_polling()

if __name__ == "__main__":
    main()
