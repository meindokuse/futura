from functools import wraps
from typing import Dict, Type
from enum import Enum
from sqlalchemy.orm import DeclarativeBase

from src.schemas.logs import LogsCreate
from src.utils.log_enum import LogType, LogAction

from typing import Dict
from enum import Enum
from functools import wraps
from sqlalchemy.orm import DeclarativeBase

# Словарь соответствия LogType и названий репозиториев в UoW
LOG_TYPE_TO_REPO: Dict[LogType, str] = {
    LogType.EMPLOYEE: "employers",
    LogType.MANUAL: "card",
    LogType.SCHEDULE: "work_day",
    LogType.RESIDENTS: "residents",
    LogType.EVENTS: "event",
}

LOG_TYPE_TO_NAME: Dict[LogType, str] = {
    LogType.EMPLOYEE: "сотрудника",
    LogType.MANUAL: "методичку",
    LogType.SCHEDULE: "смену",
    LogType.RESIDENTS: "постоянного гостя",
    LogType.EVENTS: "событие",
}


def log_action(log_type: LogType, log_action: LogAction):
    """
    Универсальный декоратор для логирования действий
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Ищем uow в аргументах
            uow = None
            for arg in args:
                if hasattr(arg, '__class__') and hasattr(arg.__class__, 'commit'):
                    uow = arg
                    break

            if not uow:
                raise ValueError("UnitOfWork not found in arguments")

            # Анализируем сигнатуру функции для получения параметров
            import inspect
            sig = inspect.signature(func)
            params = sig.parameters

            # Получаем значения параметров из args и kwargs
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Ищем admin_id и object_id в параметрах
            admin_id = None
            object_id = None

            if 'admin_id' in bound_args.arguments:
                admin_id = bound_args.arguments['admin_id']
            if 'id' in bound_args.arguments:
                object_id = bound_args.arguments['id']

            # Альтернативные названия параметров
            if not object_id:
                for param_name in ['object_id', 'event_id', 'card_id', 'resident_id', 'employee_id']:
                    if param_name in bound_args.arguments:
                        object_id = bound_args.arguments[param_name]
                        break

            if not admin_id or not object_id:
                raise ValueError(
                    f"admin_id and object_id must be provided. Got admin_id={admin_id}, object_id={object_id}")

            # Получаем название репозитория
            repo_name = LOG_TYPE_TO_REPO.get(log_type)
            if not repo_name:
                raise ValueError(f"Repository mapping not found for LogType: {log_type}")

            async with uow:
                repo = getattr(uow, repo_name, None)
                if not repo:
                    raise ValueError(f"Repository {repo_name} not found in UnitOfWork")

                # Получаем объект для логирования
                if log_type == LogType.EVENTS:
                    object_instance = await repo.get_event_by_id(object_id)
                if not object_instance:
                    raise ValueError(f"Object {repo_name} with ID {object_id} not found")

            # Формируем имя объекта


            # Выполняем основную функцию
            result = await func(*args, **kwargs)

            return result

        return wrapper

    return decorator
