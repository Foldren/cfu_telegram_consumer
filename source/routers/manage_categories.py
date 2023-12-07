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
    category = await Category.filter(id=request.id, user_id=request.userID).first()

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


# @consumer(router=router, queue=telegram_queue, pattern="bank.close-user-bank-account", request=CloseBankAccountRequest)
# async def close_user_bank_account(request: CloseBankAccountRequest):
#     pa = await PaymentAccount.filter(id=request.paymentAccountID, user_bank__user_id=request.userID).first()
#     pa.status = 0
#     await pa.save()
#
#     return CloseBankAccountResponse(id=request.paymentAccountID)
#
#
# @consumer(router=router, queue=telegram_queue, pattern="bank.get-user-account-balances", request=AccountBalancesRequest)
# async def get_user_account_balances(request: AccountBalancesRequest):
#     selected_pa = await PaymentAccount \
#         .filter(user_bank__user_id=request.userID, legal_entity_id__in=request.legalEntities) \
#         .select_related("user_bank__support_bank")
#
#     # Пробегаемся по счетам и складываем балансы для каждого банка -----------------------------------------------------
#     list_bank_balances = {}
#     for pa in selected_pa:
#         pa_sup_bank_name = pa.user_bank.support_bank.name.split(".")[0]
#         if pa_sup_bank_name not in list_bank_balances:
#             list_bank_balances[pa_sup_bank_name] = Money(amount=pa.balance, currency="RUB")
#         else:
#             list_bank_balances[pa_sup_bank_name] = list_bank_balances[pa_sup_bank_name] + Money(amount=pa.balance,
#                                                                                                 currency="RUB")
#
#     list_d_balances = []
#     for bank, balance in list_bank_balances.items():
#         d_balance = DBalance(balance=balance.amount, currency="RUB")
#         list_d_balances.append(DAccountBalance(bank=bank, balance=d_balance))
#
#     return AccountBalancesResponse(balances=list_d_balances)
#
#
# @consumer(router=router, queue=telegram_queue, pattern="bank.get-user-expenses")
# async def get_user_expenses():
#     return 'Get user expenses handler is working!'
#
#
# @consumer(router=router, queue=telegram_queue, pattern="bank.get-user-cash-balances-on-hand")
# async def get_user_cash_balances_on_hand():
#     return 'Get user cash balances on hand handler is working!'
#
#
# @consumer(router=router, queue=telegram_queue, pattern='bank.user-add-current-account',
#           request=UserAddCurrentAccountRequest)
# async def create_user_payment_accounts(request: UserAddCurrentAccountRequest):
#     user_bank = await UserBank.filter(id=request.userBankId, user_id=request.userId).first()
#
#     list_new_pa = []
#     for number in request.currentAccounts:
#         list_new_pa.append(PaymentAccount(
#             legal_entity_id=request.legalEntityId,
#             user_bank_id=request.userBankId,
#             number=number)
#         )
#
#     await user_bank.payment_accounts.add(*list_new_pa)
#
#     # return UserAddCurrentAccountResponse()
#
#
# @consumer(router=router, queue=telegram_queue, pattern='test_date_default')
# async def test_date_default():
#     await PaymentAccount.create(
#         legal_entity_id="123",
#         user_bank_id=1,
#         number=str(random.randint(1, 900))
#     )
