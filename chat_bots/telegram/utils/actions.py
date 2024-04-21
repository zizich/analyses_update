class Action:
    EN: str
    RU: str

    def __eq__(self, other):
        if issubclass(other, Action):
            return other.EN.lower() == self.EN.lower() or other.RU.lower() == self.RU.lower()

        if isinstance(other, str):
            return other.lower() == self.EN.lower() or other.lower() == self.RU.lower()


class Start(Action):
    EN = 'Start'
    RU = 'Старт'


class Cancel(Action):
    EN = 'Cancel'
    RU = 'Отменить'


class Approve(Action):
    EN = 'Approve'
    RU = 'Подтвердить'


class Edit(Action):
    EN = 'Edit'
    RU = 'Редактировать'
