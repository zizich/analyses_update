import logging
import sys

from aiogram import Router, Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from adapters.base import BaseAdapter
from adapters.telegram.routes import routes
from settings import WEBHOOK_DOMAIN, WEB_HOOK_PORT, WEBHOOK_PATH, TOKEN, WEB_SERVER_HOST, WEB_SERVER_PORT

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logging.getLogger('aiogram').setLevel(logging.DEBUG)


class TelegramAdapter(BaseAdapter):

    def __init__(self):
        self.bot: Bot | None = None
        self.dispatcher: Dispatcher | None = None

        self.router = Router()
        self.webhook_url = f"{WEBHOOK_DOMAIN}:{WEB_HOOK_PORT}{WEBHOOK_PATH}"

    async def run(self) -> None:
        self.bot = Bot(TOKEN)
        self.dispatcher = Dispatcher()

        self.register_handlers()
        self.setup_dispatcher()

        web_app = web.Application()
        self.setup_webhook_request_handler(web_app)
        setup_application(web_app, self.dispatcher, bot=self.bot)

        await web._run_app(  # noqa
            app=web_app,
            host=WEB_SERVER_HOST,
            port=WEB_SERVER_PORT,
            ssl_context=self.create_ssl_context()
        )

    def setup_dispatcher(self):
        self.dispatcher.include_router(self.router)
        self.dispatcher.startup.register(self.on_startup)

    async def on_startup(self, bot: Bot) -> None:
        logging.info("Bot has been started")
        await bot.set_webhook(self.webhook_url)
        logging.info(f"Webhook has been set up: {self.webhook_url}")

    def register_handlers(self):
        for route in routes:
            self.router.message.register(*route)

    def setup_webhook_request_handler(self, web_app) -> None:
        webhook_requests_handler = SimpleRequestHandler(dispatcher=self.dispatcher, bot=self.bot)
        webhook_requests_handler.register(web_app, path=WEBHOOK_PATH)

    def create_ssl_context(self):
        # WEBHOOK_SSL_PRIV = "/home/user/cert/key.pem"
        # WEBHOOK_SSL_CERT = "/home/user/cert/fullchain.pem"
        # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # context.load_cert_chain(
        #     WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV
        # )
        ...
