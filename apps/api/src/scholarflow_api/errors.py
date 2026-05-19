from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from scholarflow_schemas.errors import ErrorResponse


def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    body = ErrorResponse(
        code="validation_error",
        message="Request validation failed",
        detail={"errors": exc.errors()},
    )
    return JSONResponse(status_code=422, content=body.model_dump())
