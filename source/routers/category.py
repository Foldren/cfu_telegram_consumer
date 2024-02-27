from faststream.rabbit import RabbitRouter
from money import Money
from components.requests.category import CreateCategoryRequest, UpdateCategoryRequest, DeleteCategoriesRequest, \
    GetCategoriesRequest, CashBalancesOnHandRequest
from components.responses.children import CCategory, CBalanceResponse, CCashBalanceOnHandResponse
from components.responses.category import CreateCategoryResponse, UpdateCategoryResponse, \
    DeleteCategoriesResponse, GetCategoriesResponse, CashBalancesOnHandResponse
from config import SERVICE_CATEGORIES, STATIC_CATEGORIES
from decorators import consumer
from models import Category, DataCollect
from queues import telegram_queue

router = RabbitRouter()


@consumer(router=router, queue=telegram_queue, pattern="telegram.create-category", request=CreateCategoryRequest)
async def create_category(request: CreateCategoryRequest):
    if request.parentID is not None:
        category = await Category.filter(id=request.parentID, user_id=request.userID).select_related(
            "parent",
            "parent__parent",
            "parent__parent__parent",
            "parent__parent__parent__parent",
            "parent__parent__parent__parent__parent").first()

        parent = category.parent
        list_parents = [parent]

        # Проверяем уровень вложенности очереди
        while parent is not None:
            parent = parent.parent if (parent is not None) else None
            list_parents.append(parent)

        if len(list_parents) >= 5:
            raise Exception("У категории максимальный уровень 5!")

    created_category = await Category.create(
        user_id=request.userID,
        parent_id=request.parentID,
        name=request.name
    )

    return CreateCategoryResponse(id=created_category.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.update-category", request=UpdateCategoryRequest)
async def update_category(request: UpdateCategoryRequest):
    category = await Category.filter(id=request.categoryID, user_id=request.userID).first()

    if category.status in [2, 3]:
        raise Exception("Нельзя редактировать сервисные и статические категории.")

    if request.name:
        category.name = request.name
    if request.status is not None:
        category.status = request.status

    await category.save()
    await category.refresh_from_db()

    return UpdateCategoryResponse(id=category.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.delete-categories", request=DeleteCategoriesRequest)
async def delete_categories(request: DeleteCategoriesRequest):
    categories = await Category.filter(id__in=request.categoriesID, user_id=request.userID)

    for category in categories:
        if category.status in [2, 3]:
            raise Exception("Нельзя удалить сервисные или статические категории.")

    await Category.filter(id__in=request.categoriesID, user_id=request.userID).delete()

    return DeleteCategoriesResponse(categoriesID=request.categoriesID)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-categories", request=GetCategoriesRequest)
async def get_categories(request: GetCategoriesRequest):
    # Если включены сервисные категории то проверяем есть ли они, если нет, создаем для пользователя
    if request.includeStatic:
        stasuses = [0, 1, 3]
        service_categories = await Category.filter(user_id=request.userID, status=2).all()

        if not service_categories:
            service_categories_obj = []

            for sc in SERVICE_CATEGORIES:
                service_categories_obj.append(Category(user_id=request.userID, status=2, name=sc))
            for sc in STATIC_CATEGORIES:
                service_categories_obj.append(Category(user_id=request.userID, status=3, name=sc))

            await Category.bulk_create(service_categories_obj, ignore_conflicts=True)
    else:
        stasuses = [0, 1]

    categories = await Category.filter(user_id=request.userID, parent_id=request.parentID, status__in=stasuses).all()
    list_categories = []

    categories_id = [c.id for c in categories]
    child_categories = await Category.filter(user_id=request.userID, parent_id__in=categories_id).all()
    categories_with_child_id = [c.parent_id for c in child_categories]

    for category in categories:
        list_categories.append(CCategory(id=category.id,
                                         name=category.name,
                                         status=category.status,
                                         hasChildren=category.id in categories_with_child_id))

    return GetCategoriesResponse(categories=list_categories)


# @consumer(router=router, queue=telegram_queue, pattern="telegram.get-lower-categories",
#           request=GetLowerCategoriesRequest)
# async def get_lower_categories(request: GetLowerCategoriesRequest):
#     categories = await Category.filter(user_id=request.userID).select_related(
#         "parent",
#         "parent__parent",
#         "parent__parent__parent",
#         "parent__parent__parent__parent",
#         "parent__parent__parent__parent__parent").all()
#
#     categories.sort(key=lambda c: c.id)
#
#     # Генерируем очереди для категорий
#     categories_with_q = []
#     for category in categories:
#         category_with_q = {"id": category.id, "name": category.name, "queue": []}
#         parent = category.parent
#
#         while parent is not None:
#             category_with_q["queue"].append(parent.name)
#             parent = parent.parent if (parent is not None) else None
#
#         category_with_q["queue"].reverse()
#
#         categories_with_q.append(category_with_q)
#
#     # Оставляем только низшие
#     lower_categories = []
#     for i, category in enumerate(categories_with_q):
#         is_lower = True
#         for category_2 in categories_with_q:
#             if category['name'] in category_2['queue']:
#                 is_lower = False
#                 break
#
#         if is_lower:
#             lower_categories.append(category)
#
#     res_categories = []
#     for category in lower_categories:
#         res_categories.append(DLowerCategory(id=category["id"], name=category["name"], queue=category['queue']))
#
#     return GetLowerCategoriesResponse(categories=res_categories)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-user-expenses")
async def get_user_expenses():
    return 'Get user expenses handler is working!'


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-user-cash-balances-on-hand",
          request=CashBalancesOnHandRequest)
async def get_user_cash_balances_on_hand(request: CashBalancesOnHandRequest):
    users_id = request.usersID
    legal_entities_id = request.legalEntitiesID

    users_dc: list[DataCollect] = await DataCollect \
        .filter(executor_id__in=users_id, support_wallet_id=1) \
        .order_by("executor_id") \
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
            CCashBalanceOnHandResponse(userID=key, balance=CBalanceResponse(value.amount, "RUB"))
        )

    return CashBalancesOnHandResponse(cashBalancesOnHand=cash_balances_response)
