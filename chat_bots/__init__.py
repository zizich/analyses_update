import abc


class Adapter(abc.ABC):
    async def run(self): ...
