from typing import Any
from faststream import Context
from faststream.rabbit import RabbitQueue, RabbitRouter
from components.responses.rpc import RpcResponse, RpcError


def consumer(router: RabbitRouter, queue: RabbitQueue, pattern: str, request: Any = Any):
    def _rpc_consumer_dec(func):
        @router.subscriber(queue=queue, filter=lambda msg: msg.decoded_body['pattern'] == pattern)
        async def _wrapper(request_obj: request = Context("message.decoded_body.data", cast=True)):
            response = RpcResponse()
            try:
                if request is not Any:
                    response.data = await func(request_obj)
                else:
                    response.data = await func()
            except Exception as e:
                response.error = RpcError(message=str(e))
                response.data = None

            json_response = await response.get_json()
            return json_response

        return _wrapper

    return _rpc_consumer_dec
