from datetime import datetime, timedelta
from faststream.rabbit import RabbitRouter
from components.requests.custom import LinkerGetDashboardPnlRequest
from components.responses.children import CLinkerGetDashboardPnlExpenses, CLinkerValue
from components.responses.custom import LinkerGetDashboardPnlResponse
from config import STATIC_CATEGORIES, INN_MARKETPLACES
from db_models.bank import DataCollect as BankDataCollect
from db_models.telegram import DataCollect as TgDataCollect, Counterparty
from decorators import consumer
from queues import telegram_queue

router = RabbitRouter()


@consumer(router=router, queue=telegram_queue, pattern="telegram.get-dashboard-pnl",
          request=LinkerGetDashboardPnlRequest)
async def get_dashboard_pnl(request: LinkerGetDashboardPnlRequest) -> LinkerGetDashboardPnlResponse:
    cur_start_date = datetime.strptime(request.dateFrom, "%Y-%m-%d")
    cur_end_date = datetime.strptime(request.dateTo, "%Y-%m-%d")
    prev_start_date = cur_start_date - (cur_end_date - cur_start_date) - timedelta(days=1)

    # Подгружаем данные из бд
    bank_data_collects = await BankDataCollect.filter(payment_account__legal_entity_id__in=request.legalEntitiesID,
                                                      payment_account__user_bank__user_id=request.userID,
                                                      trxn_date__range=[prev_start_date, cur_end_date]
                                                      ).select_related("payment_account")

    tg_data_collects = await TgDataCollect.filter(executor_id__in=request.legalEntitiesID,
                                                  category__user_id=request.userID,
                                                  transaction__date__range=[prev_start_date, cur_end_date]
                                                  ).select_related("category", "transaction")

    counterparties = await Counterparty.filter(user_id=request.userID).select_related("category").all()

    # Формируем responses
    expenses = CLinkerGetDashboardPnlExpenses(
        anotherExpenses=CLinkerValue(prevValue=0, currentValue=0),
        package=CLinkerValue(prevValue=0, currentValue=0),
        rent=CLinkerValue(prevValue=0, currentValue=0),
        salary=CLinkerValue(prevValue=0, currentValue=0)
    )
    response = LinkerGetDashboardPnlResponse(anotherRevenue=CLinkerValue(prevValue=0, currentValue=0),
                                             expenses=expenses)

    # Сопоставляем категории и ИНН контрагентов
    counterparties_inn_category = {}
    for cp in counterparties:
        counterparties_inn_category[cp.inn] = cp.category.name

    # Пробегаемся по data_collects мс банка
    for dc in bank_data_collects:
        if cur_start_date.date() <= dc.trxn_date <= cur_end_date.date():
            option_param = "currentValue"
        else:
            option_param = "prevValue"

        if dc.type == "Расход":
            # Если контрагент распределен
            if dc.counterparty_inn in counterparties_inn_category:
                category_name = counterparties_inn_category[dc.counterparty_inn]
                # Если одна из static категорий
                if category_name in STATIC_CATEGORIES:
                    match category_name:
                        case "Зарплата":
                            new_val = getattr(expenses.salary, option_param) + dc.amount
                            setattr(expenses.salary, option_param, new_val)
                        case "Аренда":
                            new_val = getattr(expenses.rent, option_param) + dc.amount
                            setattr(expenses.rent, option_param, new_val)
                        case "Упаковка":
                            new_val = getattr(expenses.package, option_param) + dc.amount
                            setattr(expenses.package, option_param, new_val)
            # Если контрагент не распределен
            else:
                new_val = getattr(expenses.anotherExpenses, option_param) + dc.amount
                setattr(expenses.anotherExpenses, option_param, new_val)

        elif dc.type == "Доход":
            # Если контрагент не из маркетплейсов
            if int(dc.counterparty_inn) not in INN_MARKETPLACES:
                new_val = getattr(response.anotherRevenue, option_param) + dc.amount
                setattr(response.anotherRevenue, option_param, new_val)

    # Пробегаемся по data_collects мс telegram
    for dc in tg_data_collects:
        if cur_start_date.date() <= dc.transaction.date <= cur_end_date.date():
            option_param = "currentValue"
        else:
            option_param = "prevValue"

        if dc.type == "Расход":
            # Если одна из static категорий
            if dc.category.name in STATIC_CATEGORIES:
                match dc.category.name:
                    case "Зарплата":
                        new_val = getattr(expenses.salary, option_param) + dc.amount
                        setattr(expenses.salary, option_param, new_val)
                    case "Аренда":
                        new_val = getattr(expenses.rent, option_param) + dc.amount
                        setattr(expenses.rent, option_param, new_val)
                    case "Упаковка":
                        new_val = getattr(expenses.package, option_param) + dc.amount
                        setattr(expenses.package, option_param, new_val)
            else:
                new_val = getattr(response.anotherRevenue, option_param) + dc.amount
                setattr(response.anotherRevenue, option_param, new_val)

    response.expenses = expenses

    print(response)
    return response
