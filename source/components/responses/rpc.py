from dataclasses import dataclass, asdict
from simplejson import dumps
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
        return dumps(asdict(self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
