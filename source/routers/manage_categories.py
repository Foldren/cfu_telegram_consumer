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


# @router.subscriber(queue=telegram_queue)
# async def purge_messages():
#     pass


@consumer(router=router, queue=telegram_queue, pattern="telegram.create-category", request=CreateCategoryRequest)
async def create_category(request: CreateCategoryRequest):
    created_category = await Category.create(
        user_id=request.userID,
        parent_id=request.parentID,
        name=request.name,
        level=request.level,

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
        list_categories.append(
            DCategory(id=category.id, name=category.name, status=category.status, level=category.level)
        )

    return GetCategoriesResponse(categories=list_categories)
