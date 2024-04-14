from adapters.telegram import TelegramAdapter
import asyncio


if __name__ == "__main__":
    adapter = TelegramAdapter()
    asyncio.run(adapter.run())

# ssh -p 443 -R0:localhost:8080 -L4300:localhost:4300 -o StrictHostKeyChecking=no -o ServerAliveInterval=30 Qrw8dxb8ds5@a.pinggy.io