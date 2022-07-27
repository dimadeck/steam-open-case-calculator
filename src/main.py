from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from api import router
from api.middleware.orm_error import ExceptionSQL, sql_exception_handler


def get_application():
    application = FastAPI(
        debug=True,
        title='Steam Open Case Calculator',
        docs_url='/docs',
        version='0.0.1'
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=['*']
    )

    application.add_exception_handler(ExceptionSQL, sql_exception_handler)
    application.include_router(router, prefix="/api/v1")

    return application


app = get_application()
