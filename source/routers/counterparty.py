from faststream.rabbit import RabbitRouter
from tortoise.expressions import Q
from components.requests.counterparty import CreateCounterpartyRequest, DeleteCounterpartiesRequest, \
    GetCounterpartiesRequest, UpdateCounterpartyRequest
from components.responses.children import CCounterparty
from components.responses.counterparty import CreateCounterpartyResponse, DeleteCounterpartiesResponse, \
    GetCounterpartiesResponse, UpdateCounterpartyResponse
from components.decorators import consumer
from db_models.telegram import Counterparty
from components.queues import telegram_queue

router = RabbitRouter()


@consumer(router=router, queue=telegram_queue, pattern="telegram.create-counterparty",
          request=CreateCounterpartyRequest)
async def create_counterparty(request: CreateCounterpartyRequest) -> CreateCounterpartyResponse:
    """
    Роут на создание контрагента, с проверкой на существование для данного юзера
    :param request: request объект на создание контрагента CreateCounterpartyRequest
    :return: response объект на создание контрагента CreateCounterpartyResponse
    """

    user_counterparties_inn = await Counterparty.filter(user_id=request.userID).values_list("inn", flat=True)

    if request.inn not in user_counterparties_inn:
        created_counterparty = await Counterparty.create(
            user_id=request.userID,
            name=request.name,
            inn=request.inn,
            category_id=request.categoryID,
        )

        return CreateCounterpartyResponse(id=created_counterparty.id)

    else:
        raise ValueError("Контрагент с таким ИНН уже добавлен под вашим аккаунтом.")


@consumer(router=router, queue=telegram_queue, pattern="telegram.update-counterparty",
          request=UpdateCounterpartyRequest)
async def update_counterparty(request: UpdateCounterpartyRequest) -> UpdateCounterpartyResponse:
    """
    Роут на обновление контрагента, с проверкой на существование по ИНН для данного юзера
    :param request: request объект на обновление контрагента UpdateCounterpartyRequest
    :return: response объект на обновление контрагента UpdateCounterpartyResponse
    """

    user_counterparties_inn = await Counterparty.filter(user_id=request.userID).values_list("inn", flat=True)

    if request.inn not in user_counterparties_inn:
        counterparty = await Counterparty.filter(id=request.counterpartyID, user_id=request.userID).first()

        if request.name:
            counterparty.name = request.name
        if request.inn:
            counterparty.inn = request.inn
        if request.categoryID:
            counterparty.category_id = request.categoryID

        await counterparty.save()
        await counterparty.refresh_from_db()

        return UpdateCounterpartyResponse(id=counterparty.id)

    else:
        raise ValueError("Контрагент с таким ИНН уже добавлен под вашим аккаунтом.")


@consumer(router=router, queue=telegram_queue, pattern="telegram.delete-counterparties",
          request=DeleteCounterpartiesRequest)
async def delete_counterparties(request: DeleteCounterpartiesRequest) -> DeleteCounterpartiesResponse:
    """
    Роут на удаление контрагентов
    :param request: request объект на удаление контрагентов DeleteCounterpartiesRequest
    :return: response объект на удаление контрагентов DeleteCounterpartiesResponse
    """

    await Counterparty.filter(id__in=request.counterpartiesID, user_id=request.userID).delete()

    return DeleteCounterpartiesResponse(counterpartiesID=request.counterpartiesID)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-counterparties", request=GetCounterpartiesRequest)
async def get_counterparties(request: GetCounterpartiesRequest) -> GetCounterpartiesResponse:
    """
    Роут на получение списка контрагентов, с возможностью выбора showMode: all - все,
    distributed - распределенные по категориям, not_distributed - не распределенные
    :param request: request объект на получение списка контрагентов GetCounterpartiesRequest
    :return: response объект на получение списка контрагентов GetCounterpartiesResponse
    """

    match request.showMode:
        case "distributed":
            expr = Q(user_id=request.userID) & Q(category_id__not_isnull=True)
        case "not_distributed":
            expr = Q(user_id=request.userID) & Q(category_id__isnull=True)
        case "all":
            expr = Q(user_id=request.userID)
        case _:
            raise ValueError("Доступные значения поля showMode: all - все, distributed - распределенные по категориям,"
                             "not_distributed - не распределенные")

    counterparties = await Counterparty.filter(expr).select_related("category").all()
    list_counterparties = []

    for counterparty in counterparties:
        list_counterparties.append(
            CCounterparty(id=counterparty.id,
                          name=counterparty.name,
                          inn=counterparty.inn,
                          categoryID=counterparty.category.id if counterparty.category is not None else None,
                          categoryName=counterparty.category.name if counterparty.category is not None else None
                          )
        )

    return GetCounterpartiesResponse(counterparties=list_counterparties)
