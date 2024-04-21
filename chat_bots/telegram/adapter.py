import logging

from aiogram import Bot, Router, Dispatcher
from aiogram.dispatcher.event.handler import CallbackType
from aiogram.filters import Command
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from chat_bots import Adapter
from chat_bots.telegram import UserCase, Routes
from settings import Config


class TelegramAdapter(Adapter):

    def __init__(self, config: type[Config], routes: type[Routes]):
        self.config = config
        self.routes = routes

        self.bot = Bot(config.TELEGRAM_TOKEN)
        self.router = Router()
        self.dispatcher = self._build_dispatcher(self.router)
        self.web_app = self._build_web_app(self.bot, self.dispatcher)

    async def run(self) -> None:
        await web._run_app(  # noqa
            app=self.web_app,
            host=self.config.SERVER_HOST,
            port=self.config.SERVER_PORT,
            ssl_context=self._create_ssl_context()
        )

    async def set_routes(self, bot: Bot) -> None:
        simple_commands = self._set_commands(self.routes.commands)
        user_case_commands = self._set_user_cases(self.routes.user_cases)
        to_set = simple_commands + user_case_commands
        await bot.set_my_commands(to_set)
        logging.info(f"Commands has been set: {to_set}")

    def _set_commands(self, commands: dict[CallbackType, BotCommand]) -> list[BotCommand]:
        for handler, bot_command in commands.items():
            self.router.message.register(handler, Command(bot_command))
        return list(commands.values())

    def _set_user_cases(self, user_cases: dict[UserCase, BotCommand]) -> list[BotCommand]:
        for user_case, bot_command in user_cases.items():
            self.dispatcher.include_router(user_case.router)
            self.router.message.register(user_case.entrypoint, Command(bot_command))
        return list(user_cases.values())

    def _build_dispatcher(self, router: Router) -> Dispatcher:
        dispatcher = Dispatcher()
        dispatcher.include_router(router)
        dispatcher.startup.register(self._on_startup)
        return dispatcher

    async def _on_startup(self, bot: Bot) -> None:
        await bot.set_webhook(self.config.WEBHOOK_URL)
        logging.info(f"Webhook has been set up: {self.config.WEBHOOK_URL}")
        await self.set_routes(bot)

    def _build_web_app(self, bot: Bot, dispatcher: Dispatcher) -> web.Application:
        app = web.Application()
        SimpleRequestHandler(dispatcher, bot).register(app, path=self.config.WEBHOOK_PATH)
        setup_application(app, dispatcher, bot=bot)
        return app

    def _create_ssl_context(self):
        # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # context.load_cert_chain(self.config.webhook_ssl_cert, self.config.webhook_ssl_priv)
        # return context
        ...
