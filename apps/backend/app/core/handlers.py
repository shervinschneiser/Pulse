from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import PulseException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(PulseException)
    async def pulse_exception_handler(
        request: Request,
        exc: PulseException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        return JSONResponse(
            status_code=422,
            content={
                "detail": exc.errors(),
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal Server Error",
            },
        )
