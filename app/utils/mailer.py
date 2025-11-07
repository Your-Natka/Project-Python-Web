import asyncio

async def send_verification_email(email: str, token: str):
    # У реальному проєкті тут інтегрується SMTP або SendGrid
    print(f"[MAILER] Надсилаємо лист підтвердження на {email} з токеном: {token}")
    await asyncio.sleep(0.5)