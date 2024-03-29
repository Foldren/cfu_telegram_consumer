from dataclasses import dataclass, asdict
from json import dumps
from typing import Any


@dataclass
class RpcError:
    message: str
    statusCode: int = 422


@dataclass
class RpcResponse:
    data: Any = None
    error: RpcError = None

    async def get_json(self):
        """
        Функция для получения rpc response в формате json, исключая поля со значениями None
        :return: response в формате json
        """
        return dumps(asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
