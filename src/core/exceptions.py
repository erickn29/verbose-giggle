from typing import Any

from fastapi import HTTPException


class BaseHTTPException(HTTPException):

    exc_message = {
        400: "Ошибка запроса",
        401: "Ошибка аутентификации",
        404: "Объект не найден",
        422: "Ошибка валидации входных данных",
        403: "Недостаточно прав",
    }

    def __init__(
        self,
        status_code: int,
        msg: str = "",
        extra: str = "",
        detail: Any = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(status_code, detail, headers)
        self.status_code = status_code
        self.extra = extra
        self.msg = msg

    def get_response(self):
        if self.status_code not in self.exc_message:
            raise KeyError(f"Статус код <{self.status_code}> не найден")
        return {
            "msg": (
                self.exc_message.get(self.status_code) if not self.msg else self.msg
            ),
            "extra": {"detail": self.extra},
        }


def exception(
    status_code: int,
    msg: str = "",
    extra: str = "",
) -> BaseHTTPException:
    return BaseHTTPException(status_code=status_code, msg=msg, extra=extra)
