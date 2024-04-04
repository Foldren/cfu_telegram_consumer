from faststream.rabbit import RabbitRouter
from money import Money
from components.requests.category import CreateCategoryRequest, UpdateCategoryRequest, DeleteCategoriesRequest, \
    GetCategoriesRequest, CashBalancesOnHandRequest
from components.responses.children import CCategory, CBalanceResponse, CCashBalanceOnHandResponse
from components.responses.category import CreateCategoryResponse, UpdateCategoryResponse, \
    DeleteCategoriesResponse, GetCategoriesResponse, CashBalancesOnHandResponse
from config import STATIC_CATEGORIES, SERVICE_CATEGORIES
from components.decorators import consumer
from db_models.telegram import Category, DataCollect
from components.queues import telegram_queue

router = RabbitRouter()


@consumer(router=router, queue=telegram_queue, pattern="telegram.create-category", request=CreateCategoryRequest)
async def create_category(request: CreateCategoryRequest) -> CreateCategoryResponse:
    """
    Роут на создание категории. Также проверяет на уровень вложенности (максимальный - 5)
    :param request: request объект на создание категории CreateCategoryRequest
    :return: response объект на создание категории CreateCategoryResponse
    """

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
        name=request.name,
        iconID=request.iconID
    )

    return CreateCategoryResponse(id=created_category.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.update-category", request=UpdateCategoryRequest)
async def update_category(request: UpdateCategoryRequest) -> UpdateCategoryResponse:
    """
    Роут на обновление категории. Также стоит ограничение на обновление сервисных и статических категорий
    :param request: request объект на обновление категории UpdateCategoryRequest
    :return: response объект на обновление категории UpdateCategoryResponse
    """

    category = await Category.filter(id=request.categoryID, user_id=request.userID).first()

    if category.status in [2, 3]:
        raise Exception("Нельзя редактировать сервисные и статические категории.")

    if request.name:
        category.name = request.name
    if request.status is not None:
        category.status = request.status
    if request.iconID is not None:
        category.iconID = request.iconID

    await category.save()
    await category.refresh_from_db()

    return UpdateCategoryResponse(id=category.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.delete-categories", request=DeleteCategoriesRequest)
async def delete_categories(request: DeleteCategoriesRequest) -> DeleteCategoriesResponse:
    """
    Роут на удаление категории. Также стоит ограничение на удаление сервисных и статических категорий
    :param request: request объект на удаление категории DeleteCategoryRequest
    :return: response объект на удаление категории DeleteCategoryResponse
    """

    categories = await Category.filter(id__in=request.categoriesID, user_id=request.userID)

    for category in categories:
        if category.status in [2, 3]:
            raise Exception("Нельзя удалить сервисные или статические категории.")

    await Category.filter(id__in=request.categoriesID, user_id=request.userID).delete()

    return DeleteCategoriesResponse(categoriesID=request.categoriesID)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-categories", request=GetCategoriesRequest)
async def get_categories(request: GetCategoriesRequest) -> GetCategoriesResponse:
    """
    Роут на получение списка категорий. Проверяет есть ли статические и сервисные категории, если нет, создает
    :param request: request объект на получение списка категорий GetCategoriesRequest
    :return: response объект на получение списка категорий GetCategoriesResponse
    """

    # Если включены сервисные категории, то проверяем есть ли они, если нет, создаем для пользователя
    if request.includeStatic:
        stasuses = [0, 1, 3]
        sc_categories = await Category.filter(user_id=request.userID, status__in=[2, 3]).all()

        has_static_cs = False
        has_service_cs = False

        for category in sc_categories:
            if category.status == 2:
                has_service_cs = True
            if category.status == 3:
                has_static_cs = True

        # Если есть статические категории или сервисные
        if not has_static_cs or not has_service_cs:
            sc_categories_obj = []
            if not has_static_cs:
                for sc in STATIC_CATEGORIES:
                    sc_categories_obj.append(Category(user_id=request.userID, status=3, name=sc))

            if not has_service_cs:
                for sc in SERVICE_CATEGORIES:
                    sc_categories_obj.append(Category(user_id=request.userID, status=2, name=sc))

            await Category.bulk_create(sc_categories_obj, ignore_conflicts=True)
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
                                         hasChildren=category.id in categories_with_child_id,
                                         iconID=category.iconID))

    return GetCategoriesResponse(categories=list_categories)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-user-cash-balances-on-hand",
          request=CashBalancesOnHandRequest)
async def get_user_cash_balances_on_hand(request: CashBalancesOnHandRequest) -> CashBalancesOnHandResponse:
    """
    Роут на получение остатка на счетах ЮР лиц
    :param request: request объект на получение остатка на счетах ЮР лиц CashBalancesOnHandRequest
    :return: response объект на получение остатка на счетах ЮР лиц CashBalancesOnHandResponse
    """

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
