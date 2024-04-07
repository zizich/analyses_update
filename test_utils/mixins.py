from . import factories as f
from db.models.users import User


class FactoryMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_user(self, **kwargs) -> User:
        return f.create_user(session=self.session, **kwargs)

    @staticmethod
    def create_inline_keyboard(**kwargs):
        return f.create_inline_keyboard(**kwargs)
