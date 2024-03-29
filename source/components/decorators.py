from typing import Any
from faststream import Context, Logger
from faststream.rabbit import RabbitQueue, RabbitRouter
from components.responses.rpc import RpcResponse, RpcError


def consumer(router: RabbitRouter, queue: RabbitQueue, pattern: str, request: Any = Any):
    """
    Декоратор для работы с микросервисной архитектурой платформы Управляйка, берет 'pattern' из payload
    и матчит по нему. Также передает request из запроса в формате DataClass.
    :param router: роутер консьюмера
    :param queue: очередь
    :param pattern: паттерн для обработчика
    :param request: объект DataClass request
    :return:
    """

    def _rpc_consumer_dec(func):
        @router.subscriber(queue=queue, filter=lambda msg: msg.decoded_body['pattern'] == pattern)
        async def _wrapper(logger: Logger, request_obj: request = Context("message.decoded_body.data", cast=True)):
            response = RpcResponse()
            try:
                if request is not Any:
                    response.data = await func(request_obj)
                else:
                    response.data = await func()
            except Exception as e:
                logger.error(e)
                response.error = RpcError(message=str(e))
                response.data = None

            json_response = await response.get_json()
            return json_response

        return _wrapper

    return _rpc_consumer_dec
