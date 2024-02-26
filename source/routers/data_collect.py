from datetime import datetime
from faststream.rabbit import RabbitRouter
from tortoise.expressions import Q
from components.requests.data_collect import GetDataCollectsRequest
from components.responses.children import CDataCollectResponse
from components.responses.data_collect import GetDataCollectsResponse
from decorators import consumer
from models import DataCollect
from queues import telegram_queue

router = RabbitRouter()


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-data-collects", request=GetDataCollectsRequest)
async def get_data_collects(request: GetDataCollectsRequest):
    start_date = datetime.strptime(request.dateFrom, "%Y-%m-%d")
    end_date = datetime.strptime(request.dateTo, "%Y-%m-%d")

    expr = (Q(executor_id__in=request.legalEntitiesID) &
            Q(category__user_id=request.userID) &
            Q(transaction__date__range=[start_date, end_date])
            )

    data_collects = await DataCollect.filter(expr).select_related("category", "transaction")

    list_data_collects = []
    for dc in data_collects:
        dc_date = dc.transaction.date.strftime("%Y-%m-%d")
        list_data_collects.append(CDataCollectResponse(legalEntityID=dc.executor_id, categoryName=dc.category.name,
                                                       amount=dc.amount, type=dc.type, date=dc_date))

    return GetDataCollectsResponse(data_collects=list_data_collects)
