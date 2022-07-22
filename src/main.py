from fastapi import FastAPI
from api import router


def get_application():
    application = FastAPI(
        debug=True,
        title='Inventory Calculator',
        docs_url='/docs',
        version='0.0.1'
    )

    application.include_router(router, prefix="/api/v1")

    return application


app = get_application()
