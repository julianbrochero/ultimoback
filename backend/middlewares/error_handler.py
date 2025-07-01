from fastapi import Request
from fastapi.responses import JSONResponse

class ErrorHandler:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": str(e)}
            )