from faststream.rabbit import RabbitRouter
from tortoise.expressions import Q

from components.requests.counterparty import CreateCounterpartyRequest, DeleteCounterpartiesRequest, \
    GetCounterpartiesRequest, UpdateCounterpartyRequest, BindCounterpartyCategoryRequest
from components.responses.children import CCounterparty
from components.responses.counterparty import CreateCounterpartyResponse, DeleteCounterpartiesResponse, \
    GetCounterpartiesResponse, UpdateCounterpartyResponse, BindCounterpartyCategoryResponse
from decorators import consumer
from db_models.telegram import Counterparty
from queues import telegram_queue

router = RabbitRouter()


@consumer(router=router, queue=telegram_queue, pattern="telegram.bind-counterparties-category",
          request=BindCounterpartyCategoryRequest)
async def bind_counterparties_category(request: BindCounterpartyCategoryRequest):
    counterparties = await Counterparty.filter(id__in=request.counterpartiesID, user_id=request.userID).all()

    for c in counterparties:
        c.category_id = request.categoryID

    await Counterparty.bulk_update(counterparties, fields=['category_id'])

    return BindCounterpartyCategoryResponse(counterpartiesID=request.counterpartiesID)


@consumer(router=router, queue=telegram_queue, pattern="telegram.create-counterparty",
          request=CreateCounterpartyRequest)
async def create_counterparty(request: CreateCounterpartyRequest):
    created_counterparty = await Counterparty.create(
        user_id=request.userID,
        name=request.name,
        inn=request.inn,
        category_id=request.categoryID,
    )

    return CreateCounterpartyResponse(id=created_counterparty.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.update-counterparty",
          request=UpdateCounterpartyRequest)
async def update_counterparty(request: UpdateCounterpartyRequest):
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


@consumer(router=router, queue=telegram_queue, pattern="telegram.delete-counterparties",
          request=DeleteCounterpartiesRequest)
async def delete_counterparties(request: DeleteCounterpartiesRequest):
    await Counterparty.filter(id__in=request.counterpartiesID, user_id=request.userID).delete()

    return DeleteCounterpartiesResponse(counterpartiesID=request.counterpartiesID)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-counterparties", request=GetCounterpartiesRequest)
async def get_counterparties(request: GetCounterpartiesRequest):
    expr = Q(user_id=request.userID) & Q(category_id__isnull=True) if request.showNotDistributed else (
        Q(user_id=request.userID) & Q(category_id__not_isnull=True))

    counterparties = await Counterparty.filter(expr).select_related("category").all()
    list_counterparties = []

    for counterparty in counterparties:
        list_counterparties.append(
            CCounterparty(id=counterparty.id,
                          name=counterparty.name,
                          inn=counterparty.inn,
                          categoryID=None if request.showNotDistributed else counterparty.category.id,
                          categoryName=None if request.showNotDistributed else counterparty.category.name,
                          )
        )

    print(GetCounterpartiesResponse(counterparties=list_counterparties))

    return GetCounterpartiesResponse(counterparties=list_counterparties)
