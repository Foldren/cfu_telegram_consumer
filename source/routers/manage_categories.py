from faststream.rabbit import RabbitRouter
from money import Money
from components.requests.manage_categories import CreateCategoryRequest, UpdateCategoryRequest, DeleteCategoriesRequest, \
    GetCategoriesRequest, CashBalancesOnHandRequest
from components.responses.children import DCategory, DBalanceResponse, DCashBalanceOnHandResponse
from components.responses.manage_categories import CreateCategoryResponse, UpdateCategoryResponse, \
    DeleteCategoriesResponse, GetCategoriesResponse, CashBalancesOnHandResponse
from decorators import consumer
from models import Category, DataCollect
from queues import telegram_queue

router = RabbitRouter()


# @router.subscriber(queue=telegram_queue)
# async def purge_messages():
#     pass


@consumer(router=router, queue=telegram_queue, pattern="telegram.create-category", request=CreateCategoryRequest)
async def create_category(request: CreateCategoryRequest):
    created_category = await Category.create(
        user_id=request.userID,
        parent_id=request.parentID,
        name=request.name
    )

    return CreateCategoryResponse(id=created_category.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.update-category", request=UpdateCategoryRequest)
async def update_category(request: UpdateCategoryRequest):
    category = await Category.filter(id=request.categoryID, user_id=request.userID).first()

    if request.name:
        category.name = request.name
    if request.status:
        category.status = request.status

    await category.save()
    await category.refresh_from_db()

    return UpdateCategoryResponse(id=category.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.delete-categories", request=DeleteCategoriesRequest)
async def delete_categories(request: DeleteCategoriesRequest):
    await Category.filter(id__in=request.categoriesID, user_id=request.userID).delete()

    return DeleteCategoriesResponse(categoriesID=request.categoriesID)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-categories", request=GetCategoriesRequest)
async def get_categories(request: GetCategoriesRequest):
    categories = await Category.filter(user_id=request.userID, parent_id=request.parentID).all()
    list_categories = []

    for category in categories:
        list_categories.append(DCategory(id=category.id, name=category.name, status=category.status))

    return GetCategoriesResponse(categories=list_categories)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-user-expenses")
async def get_user_expenses():
    return 'Get user expenses handler is working!'


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-user-cash-balances-on-hand",
          request=CashBalancesOnHandRequest)
async def get_user_cash_balances_on_hand(request: CashBalancesOnHandRequest):
    users_id = request.usersID
    legal_entities_id = request.legalEntitiesID

    users_dc: list[DataCollect] = await DataCollect\
        .filter(executor_id__in=users_id, support_wallet_id=1)\
        .order_by("executor_id")\
        .all()

    legal_entities_dc: list[DataCollect] = await DataCollect \
        .filter(executor_id__in=legal_entities_id, support_wallet_id=1) \
        .order_by("executor_id") \
        .all()

    cash_balances = {}
    for ud in users_dc:
        for ld in legal_entities_dc:
            if ud.transaction_id == ld.transaction_id:
                if ud.executor_id in cash_balances:
                    cash_balances[ud.executor_id] += Money(amount=ud.amount, currency="RUB")
                else:
                    cash_balances[ud.executor_id] = Money(amount=ud.amount, currency="RUB")

    cash_balances_response = []
    for key, value in cash_balances.items():
        cash_balances_response.append(
            DCashBalanceOnHandResponse(userID=key, balance=DBalanceResponse(value.amount, "RUB"))
        )

    return CashBalancesOnHandResponse(cashBalancesOnHand=cash_balances_response)
