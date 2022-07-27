from typing import Optional

from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy.exc import NoResultFound, IntegrityError, DatabaseError, DBAPIError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from log import get_log_channel

_log = get_log_channel('ORM_ERROR')


class ExceptionSQL(Exception):
    def __init__(self, detail: str, sql_detail: Optional[str] = None):
        self.detail = detail
        self.sql_detail = sql_detail


def sql_exception_handler(request: Request, exc: ExceptionSQL):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail,
                 "sql_detail": exc.sql_detail}
    )


def orm_error_handler(func):
    def handle_unique_error(exc: DatabaseError, sql_detail: Optional[str] = None):
        if exc.orig.sqlstate == UniqueViolationError.sqlstate:
            raise ExceptionSQL(
                detail="Запись уже существует в базе данных",
                sql_detail=sql_detail
            )

    def handle_foreign_key_error(exc: DatabaseError, sql_detail: Optional[str] = None):
        if exc.orig.sqlstate == ForeignKeyViolationError.sqlstate:
            raise ExceptionSQL(
                detail="Произошла ошибка, связанная с внешним ключом, "
                       "возможно вы пытаетесь привязать объект к несуществующему объекту",
                sql_detail=sql_detail
            )

    def handle_not_found_error(exc: Optional[NoResultFound] = None, sql_detail: Optional[str] = None):
        raise ExceptionSQL(
            detail="Запись, которую вы ищите, отсутствует в базе данных"
        )

    def handle_db_api_error(
            exc: Optional[DBAPIError] = None,
            sql_detail: Optional[str] = None
    ):
        raise ExceptionSQL(
            detail="Произошла внутренняя ошибка базы данных при обработке запроса",
            sql_detail=sql_detail,
        )

    async def decorator(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except IntegrityError as exc:
            sql_detail = str(exc.orig).split('\n')[1]

            handle_unique_error(exc=exc, sql_detail=sql_detail)
            handle_foreign_key_error(exc=exc, sql_detail=sql_detail)

        except NoResultFound as exc:
            handle_not_found_error(exc=exc, sql_detail=None)
        except DBAPIError as exc:
            sql_detail = str(exc.orig)
            handle_db_api_error(exc=exc, sql_detail=sql_detail)
            _log.error(f'Exception: {exc}\nDetails: {sql_detail}')

    return decorator
