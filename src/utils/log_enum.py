from enum import Enum


class LogAction(Enum):
    CREATED = "добавил(а)"
    UPDATED = "редактировал(а)"
    DELETED = "удалил(а)"


class LogType(Enum):
    EMPLOYEE = 'Персонал'
    MANUAL = 'Методички'
    SCHEDULE = 'Расписание'
    RESIDENTS = 'Постоянные гости'
    EVENTS = 'События'
    FILES = 'Файлы'


class LogRelationObject:
    type: str
    name: str
