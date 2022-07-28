from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy.exc import NoResultFound, IntegrityError, DBAPIError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from log import get_log_channel

_log = get_log_channel('ORM_ERROR')


class ExceptionSQL(Exception):
    def __init__(self, exc: str):
        self.exc = exc


def sql_exception_handler(request: Request, exc: ExceptionSQL):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": exc.exc}
    )


def orm_error_handler(func):
    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as exc:
            if exc.orig.sqlstate == UniqueViolationError.sqlstate:
                raise ExceptionSQL("Объект уже существует в базе данных")
            if exc.orig.sqlstate == ForeignKeyViolationError.sqlstate:
                raise ExceptionSQL("Ошибка ключа, объекта не существует")
        except NoResultFound as exc:
            raise ExceptionSQL("Объекта не существует")
        except DBAPIError as exc:
            raise ExceptionSQL("Внутренняя ошибка базы данных")
    return decorator
