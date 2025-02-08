from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q_for_feedback = State()
    Q_for_tech_support = State()
    Q_for_info_1 = State()
    Q_for_info_2 = State()
    Q_for_notification = State()
    Q_for_notification_2 = State()
    Q_for_admin_1 = State()
    Q_for_admin_2 = State()
    Q_for_admin_3 = State()
    Q_for_admin_4 = State()
    Q_for_admin_5 = State()
    Q_for_delete_notification_1 = State()
    Q_for_delete_notification_2 = State()

