from telegram import send_telegram_message


def main():
    message = """🚀 Naukri DevOps Job Bot

Telegram connection test successful! ✅

This message was sent through:
GitHub Actions → Python → Telegram Bot

Naukri job automation is coming next.
"""

    send_telegram_message(message)


if __name__ == "__main__":
    main()
