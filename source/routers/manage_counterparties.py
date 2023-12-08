from faststream.rabbit import RabbitRouter
from components.requests.manage_categories import CreateCategoryRequest, UpdateCategoryRequest, DeleteCategoriesRequest, \
    GetCategoriesRequest
from components.responses.children import DCategory
from components.responses.manage_categories import CreateCategoryResponse, UpdateCategoryResponse, \
    DeleteCategoriesResponse, GetCategoriesResponse
from decorators import consumer
from models import Category
from queues import telegram_queue

router = RabbitRouter()


@consumer(router=router, queue=telegram_queue, pattern="telegram.create-counterparty", request=CreateCategoryRequest)
async def create_counterparty(request: CreateCategoryRequest):
    created_category = await Category.create(
        user_id=request.userID,
        parent_id=request.parentID,
        name=request.name,
        level=request.level,

    )

    return CreateCategoryResponse(id=created_category.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.update-counterparty", request=UpdateCategoryRequest)
async def update_counterparty(request: UpdateCategoryRequest):
    category = await Category.filter(id=request.id, user_id=request.userID).first()

    if request.name:
        category.name = request.name
    if request.status:
        category.status = request.status

    await category.save()
    await category.refresh_from_db()

    return UpdateCategoryResponse(id=category.id)


@consumer(router=router, queue=telegram_queue, pattern="telegram.delete-counterparties", request=DeleteCategoriesRequest)
async def delete_counterparties(request: DeleteCategoriesRequest):
    await Category.filter(id__in=request.categoriesID, user_id=request.userID).delete()

    return DeleteCategoriesResponse(categoriesID=request.categoriesID)


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-counterparties", request=GetCategoriesRequest)
async def get_counterparties(request: GetCategoriesRequest):
    categories = await Category.filter(user_id=request.userID, parent_id=request.parentID).all()
    list_categories = []

    for category in categories:
        list_categories.append(
            DCategory(id=category.id, name=category.name, status=category.status, level=category.level)
        )

    return GetCategoriesResponse(categories=list_categories)
