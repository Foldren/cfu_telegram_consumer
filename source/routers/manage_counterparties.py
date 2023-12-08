from faststream.rabbit import RabbitRouter
from components.requests.manage_categories import CreateCategoryRequest, DeleteCategoriesRequest, \
    GetCategoriesRequest
from components.requests.manage_counterparties import CreateCounterpartyRequest, DeleteCounterpartiesRequest, \
    GetCounterpartiesRequest
from components.responses.children import DCategory, DCounterparty
from components.responses.manage_categories import DeleteCategoriesResponse, GetCategoriesResponse
from components.responses.manage_counterparties import CreateCounterpartyResponse, DeleteCounterpartiesResponse, \
    GetCounterpartiesResponse
from decorators import consumer
from models import Category, Counterparty
from queues import telegram_queue

router = RabbitRouter()


@consumer(router=router, queue=telegram_queue, pattern="telegram.create-counterparty", request=CreateCounterpartyRequest)
async def create_counterparty(request: CreateCounterpartyRequest):
    created_counterparty = await Counterparty.create(
        user_id=request.userID,
        name=request.name,
        inn=request.inn,
        categoryID=request.categoryID,
    )

    return CreateCounterpartyResponse(id=created_counterparty.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.delete-counterparties", request=DeleteCounterpartiesRequest)
async def delete_counterparties(request: DeleteCounterpartiesRequest):
    await Counterparty.filter(id__in=request.counterpartiesID, user_id=request.userID).delete()

    return DeleteCounterpartiesResponse(counterpartiesID=request.counterpartiesID)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-counterparties", request=GetCounterpartiesRequest)
async def get_counterparties(request: GetCounterpartiesRequest):
    counterparties = await Counterparty.filter(user_id=request.userID).select_related("category").all()
    list_counterparties = []

    for counterparty in counterparties:
        list_counterparties.append(
            DCounterparty(id=counterparty.id,
                          name=counterparty.name,
                          inn=counterparty.inn,
                          categoryID=counterparty.category.id,
                          categoryName=counterparty.category.name,
            )
        )

    return GetCounterpartiesResponse(counterparties=list_counterparties)
