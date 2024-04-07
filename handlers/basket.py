import asyncio
import queries.search_analyse as query_search_analyses
import queries.basket as query_basket
import queries.user as query_user

import aiogram.exceptions
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.fsm_engine import States

from keyboard import delivery_in_basket, gth_after_add_date, kb_patterns
from keyboard.kb_basket_who_add import inline_choice
from keyboard.kb_basket_menu import basket_menu, basket_menu_first

router = Router(name=__name__)

transfer_date = ""  # для получения даты
pattern_global = ""  # для получения наименование шаблона


@router.message(F.text.in_("\U0001F6D2 Корзина"))
async def process_basket(message: Message):
    user_id = message.chat.id

    query_search_analyses.init_new_user_in_basket(user_id)

    #  После подтверждения заявки с БД basket.db удаляется вся инфо пользователя, соответственно при вызове сity
    #  выдает исключение, о том, что ячейка пустая. Решение: система try/except. Если, в basket.db нет инфы, мы
    #  будем брать его с cursor.db

    city = query_basket.get_city_basket(user_id)
    comment = ""
    # Комментарии пользователей ===========================================================
    try:
        comment = query_basket.get_comment_basket(user_id)
        if comment is None:
            comment = "без комментариев..."
    except (TypeError, AttributeError):
        pass
    # ====================================================================================================
    # выводим с БД basket users выбранный способ заявки
    try:
        delivery = query_basket.get_delivery_basket(user_id).upper()
    except (TypeError, AttributeError):
        delivery = "\U0000203CВыберите способ заявки!"

    # ====================================================================================================
    # инициализируем переменные
    messages = []
    profile = []
    all_prices_basket = 0
    admin_phone = ""
    admin_bank = ""
    # ===================================================================================================
    # вывод из БД списка анализов по порядковому номеру
    try:
        result = query_basket.get_added_analyses(user_id)  # БД список анализов
        # ================================================================================================
        # ==========================ВЫВОД АНАЛИЗОВ=============================
        # итерируем получаемый список заказов
        for i, (id_num, name, price, tube, readiness) in enumerate(result, start=1):
            # Добавляем номер перед каждым сообщением
            message_str = f"{i}.<b>{name.split('(')[0]}</b> - {price} р., {readiness} дн."
            messages.append(message_str)
            all_prices_basket += price

        # Присоединяем все сообщения в одну строку с помощью '\n'.json
        all_messages = "\n".join(messages)
        # ===============================================================================================

        # ================================================================================================
        # подключение к БД date_add_db для вывода в консоль выбранную ДАТУ
        try:

            date_end = query_basket.get_added_date(user_id) + " (-/+ 20 мин.)"
        except TypeError:
            date_end = "выберите дату!"
        # ================================================================================================
        # условия: если сумма анализа превышает 2500 р, то выезд бесплатный, иначе выезд - 500 р.

        sampling = 0
        out_pay = 0
        for i, (city_in_db, blood, out, address, phone, bank,
                all_sale) in enumerate(query_basket.get_info_job(), start=1):
            if city == city_in_db:
                sampling = blood
                out_pay = out
                admin_phone = phone
                admin_bank = bank

        if all_prices_basket >= 2500 or delivery == "самообращение".upper():
            check_out_at = 0
        else:
            check_out_at = out_pay

        # ==============================================================================================
        # ===============================================================================================
        # ==========================ВЫВОД ЗАКАЗЧИКА=============================
        # вывод из БД basket_db для вывода в консоль
        column_name = query_basket.get_info_users_in_basket(user_id)
        try:
            if column_name[0][2] is not None:
                for i, (user_id, fio, birth_date, phone, email, address, city, comm, exit_or_not, id_midwifery) \
                        in enumerate(column_name, start=1):
                    profile_info = f"{i}. {fio}\n{birth_date}\n{phone}\n{email}\n{address}"
                    profile.append(profile_info)

                all_profile = "\n".join(profile)
            else:
                all_profile = "\U0000203Cвыберите заказчика!"
        except (TypeError, IndexError):
            all_profile = "\U0000203Cвыберите заказчика!"

        # для логики: если, пользователь выбирает самообращение то на консоль выходит адрес пункта
        # ============================================================================================
        your_self = ""
        if delivery == "самообращение".upper():
            res = query_basket.get_info_job()
            for i, (city_go, sampling, exit_out, address, phone, bank, all_sale) in enumerate(res, start=1):
                if city_go == city:
                    your_self = "\n" + address
                    break
        # =============================================================================================
        if city is None:
            city = "\U0001F3D8"
        await message.answer(text=all_messages + "\n<b>===========================</b>"
                                                 f"\n<b>Сумма анализа:</b> {all_prices_basket} р."
                                                 f"\n<b>Забор биоматериала:</b> {sampling} р."
                                                 f"\n<b>Выезд:</b> {check_out_at} р."
                                                 f"\n<b>Общая сумма:</b> "
                                                 f"{all_prices_basket + check_out_at + sampling} р."
                                                 f"\n<b>===========================</b>"
                                                 f"\n<b>Кому:</b>"
                                                 f"\n{all_profile}"
                                                 "\n<b>===========================</b>"
                                                 f"\n<b>{delivery}</b>"
                                                 f"\n<b>Дата:</b> {date_end.split('>>')[0]}"
                                                 f"\n<b>===========================</b>"
                                                 f"\n<b>Город</b>: {city} {your_self}"
                                                 f"\n<b>===========================</b>"
                                                 f"\n<b>Комментарии:</b> {comment}"
                                                 f"\n<b>===========================</b>"
                                                 f"\n<b>Оплата: </b>переводом на"
                                                 f"\n\U0000203C{admin_bank}\U0000203C<b>{admin_phone}</b>, "
                                                 f"только после взятия биометариала",
                             reply_markup=basket_menu_first())

    except aiogram.exceptions.TelegramBadRequest:
        await message.answer(text="Корзина пуста!")


@router.callback_query(F.data == "back_to_basket_menu")
async def process_back_to_basket(call: CallbackQuery):
    user_id = call.message.chat.id
    query_search_analyses.init_new_user_in_basket(user_id)

    #  После подтверждения заявки с БД basket.db удаляется вся инфо пользователя, соответственно при вызове сity
    #  выдает исключение, о том, что ячейка пустая. Решение: система try/except. Если, в basket.db нет инфы, мы
    #  будем брать его с cursor.db

    city = query_basket.get_city_basket(user_id)
    comment = ""
    # Комментарии пользователей ===========================================================
    try:
        comment = query_basket.get_comment_basket(user_id)
        if comment is None:
            comment = "без комментариев..."
    except (TypeError, AttributeError):
        pass
    # ====================================================================================================
    # выводим с БД basket users выбранный способ заявки
    try:
        delivery = query_basket.get_delivery_basket(user_id).upper()
    except (TypeError, AttributeError):
        delivery = "\U0000203CВыберите способ заявки!"

    # ====================================================================================================
    # инициализируем переменные
    messages = []
    profile = []
    all_prices_basket = 0
    admin_phone = ""
    admin_bank = ""
    # ===================================================================================================
    # вывод из БД списка анализов по порядковому номеру
    try:
        result = query_basket.get_added_analyses(user_id)  # БД список анализов
        # ================================================================================================
        # ==========================ВЫВОД АНАЛИЗОВ=============================
        # итерируем получаемый список заказов
        for i, (id_num, name, price, tube, readiness) in enumerate(result, start=1):
            # Добавляем номер перед каждым сообщением
            message_str = f"{i}.<b>{name.split('(')[0]}</b> - {price} р., {readiness} дн."
            messages.append(message_str)
            all_prices_basket += price

        # Присоединяем все сообщения в одну строку с помощью '\n'.json
        all_messages = "\n".join(messages)
        # ===============================================================================================

        # ================================================================================================
        # подключение к БД date_add_db для вывода в консоль выбранную ДАТУ
        try:

            date_end = query_basket.get_added_date(user_id) + " (-/+ 20 мин.)"
        except TypeError:
            date_end = "выберите дату!"
        # ================================================================================================
        # условия: если сумма анализа превышает 2500 р, то выезд бесплатный, иначе выезд - 500 р.

        sampling = 0
        out_pay = 0
        for i, (city_in_db, blood, out, address, phone, bank,
                all_sale) in enumerate(query_basket.get_info_job(), start=1):
            if city == city_in_db:
                sampling = blood
                out_pay = out
                admin_phone = phone
                admin_bank = bank

        if all_prices_basket >= 2500 or delivery == "самообращение".upper():
            check_out_at = 0
        else:
            check_out_at = out_pay

        # ==============================================================================================
        # ===============================================================================================
        # ==========================ВЫВОД ЗАКАЗЧИКА=============================
        # вывод из БД basket_db для вывода в консоль
        column_name = query_basket.get_info_users_in_basket(user_id)
        try:
            if column_name[0][2] is not None:
                for i, (user_id, fio, birth_date, phone, email, address, city, comm, exit_or_not, id_midwifery) \
                        in enumerate(column_name, start=1):
                    profile_info = f"{i}. {fio}\n{birth_date}\n{phone}\n{email}\n{address}"
                    profile.append(profile_info)

                all_profile = "\n".join(profile)
            else:
                all_profile = "\U0000203Cвыберите заказчика!"
        except (TypeError, IndexError):
            all_profile = "\U0000203Cвыберите заказчика!"

        # для логики: если, пользователь выбирает самообращение то на консоль выходит адрес пункта
        # ============================================================================================
        your_self = ""
        if delivery == "самообращение".upper():
            res = query_basket.get_info_job()
            for i, (city_go, sampling, exit_out, address, phone, bank, all_sale) in enumerate(res, start=1):
                if city_go == city:
                    your_self = "\n" + address
                    break
        # =============================================================================================
        if city is None:
            city = "\U0001F3D8"
        await call.message.edit_text(text=all_messages + "\n<b>===========================</b>"
                                                         f"\n<b>Сумма анализа:</b> {all_prices_basket} р."
                                                         f"\n<b>Забор биоматериала:</b> {sampling} р."
                                                         f"\n<b>Выезд:</b> {check_out_at} р."
                                                         f"\n<b>Общая сумма:</b> "
                                                         f"{all_prices_basket + check_out_at + sampling} р."
                                                         f"\n<b>===========================</b>"
                                                         f"\n<b>Кому:</b>"
                                                         f"\n{all_profile}"
                                                         "\n<b>===========================</b>"
                                                         f"\n<b>{delivery}</b>"
                                                         f"\n<b>Дата:</b> {date_end.split('>>')[0]}"
                                                         f"\n<b>===========================</b>"
                                                         f"\n<b>Город</b>: {city} {your_self}"
                                                         f"\n<b>===========================</b>"
                                                         f"\n<b>Комментарии:</b> {comment}"
                                                         f"\n<b>===========================</b>"
                                                         f"\n<b>Оплата: </b>переводом на"
                                                         f"\n\U0000203C{admin_bank}\U0000203C<b>{admin_phone}</b>, "
                                                         f"только после взятия биометариала",
                                     reply_markup=await basket_menu())

    except aiogram.exceptions.TelegramBadRequest:
        await call.message.answer(text="Корзина пуста!")


# ==========================================================================================================
# 8.0  КОРЗИНА
#   8.1. КОМУ ЗАКАЗАТЬ?
#
#
# ==========================================================================================================
@router.callback_query(F.data == "go_to_home")
async def process_exit_or_self(call: CallbackQuery):
    global transfer_date
    user_id = call.message.chat.id

    query_basket.update_delivery_in_basket("вызов на дом", user_id)

    city = query_basket.get_city_basket(user_id)

    # Выносим из БД все даты выбранные
    date_in = query_basket.get_added_date(user_id)
    try:
        for i, (date_found) in enumerate(date_in, start=1):
            if date_found:  # сравниваем есть ли отмеченная дата у данного пользователя
                keyboard_after_add_date = InlineKeyboardBuilder()

                # создал отдельная функция для клавиатур при вызове на дом gth (go_to_home)
                kb = gth_after_add_date(keyboard_after_add_date, date_found)

                # времени кнопки-даты с БД добавляются в коллекцию
                if len(transfer_date) > 30:
                    text_delivery = "самообращение"
                else:
                    text_delivery = "вызов на дом"
                await call.message.edit_text(text="\u2705 Вы записаны на "
                                                  "\n{} \U000027A1\U0000FE0F: {}".format(text_delivery,
                                                                                         transfer_date.split("_")[0]),
                                             reply_markup=await kb)

                break

    except TypeError:
        dateAdd = query_basket.get_date_added_nurse_by_city(city)
        keyboard_gth = InlineKeyboardBuilder()
        try:
            #  функция для вывода из БД даты без часов и минут
            async def kb_gth_add_date():
                kb_builder = InlineKeyboardBuilder()
                collection_date = []
                for p, (date, done, city_i, delivery) in enumerate(dateAdd, start=1):
                    if delivery in "вызов на дом" and done in "\U0001F4CC":
                        collection_date.append(date.split(' ')[0])

                unique_date = list(set(collection_date))

                for date_i in unique_date:
                    kb_builder.button(text=date_i, callback_data=f"gthDate_{date_i}")
                kb_builder.button(text="назад \U000023EA", callback_data="exit_or_self_conversion")
                kb_builder.adjust(1)
                return kb_builder.as_markup()

            await call.message.edit_text(text=f"<b>Вызов на дом \U0001F691</b>"
                                              f"\nВыберите дату \U00002935\U0000FE0F",
                                         reply_markup=await kb_gth_add_date())
        except TypeError:
            keyboard_gth.button(text="назад \U000023EA", callback_data="exit_or_self_conversion")
            keyboard_gth.adjust(1)
            await call.message.answer(text=f"Свободных дат нет", reply_markup=keyboard_gth.as_markup())


#  обработка функции для вывода пользователям времени выбранной даты при вызове на дом
@router.callback_query(lambda c: c.data.startswith("gthDate_"))
async def process_gth_time(call: CallbackQuery):
    user_id = call.message.chat.id
    city = query_basket.get_city_basket(user_id)
    input_date = call.data.split('gthDate_')[1]

    dateAdd = query_basket.get_date_added_nurse_by_city(city)

    async def kb_gth_add_time():
        kb_builder = InlineKeyboardBuilder()
        for p, (date, done, city_i, delivery) in enumerate(dateAdd, start=1):
            if delivery in "вызов на дом" and done in "\U0001F4CC":
                if input_date in date:
                    kb_builder.button(text=f"{(date.split('_')[0]).split(' ')[1]} {done}",
                                      callback_data=f"unique_{date}")
        kb_builder.adjust(4)
        kb_builder.button(text="назад \U000023EA", callback_data="go_to_home")
        return kb_builder.as_markup()

    await call.message.edit_text(text=f"<b>Вызов на дом \U0001F691</b>"
                                      f"\nВыберите время \U00002935\U0000FE0F",
                                 reply_markup=await kb_gth_add_time())


# показать все даты по самообращению ========================================================================
@router.callback_query(F.data == "go_to_medical")  # gtm (go_to_medical)
async def process_exit_or_self(call: CallbackQuery):
    global transfer_date
    user_id = call.message.chat.id

    query_basket.update_delivery_in_basket("самообращение", user_id)

    city = query_basket.get_city_basket(user_id)

    # Выносим из БД все даты выбранные
    date_in = query_basket.get_added_date(user_id)
    try:
        async def kb_gtc_after_add_date():
            keyboard_after_add_date = InlineKeyboardBuilder()
            for o, (date_found) in enumerate(date_in, start=1):
                if date_found:  # сравниваем есть ли отмеченная дата у данного пользователя
                    # времени кнопки-даты с БД добавляются в коллекцию
                    keyboard_after_add_date.button(text="удалить дату \U00002702\U0000FE0F\U0001F564",
                                                   callback_data=f"delAddDate{transfer_date}")
            keyboard_after_add_date.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
            keyboard_after_add_date.adjust(1)
            return keyboard_after_add_date.as_markup()

        if len(transfer_date) > 30:
            text_delivery = "самообращение"
        else:
            text_delivery = "вызов на дом"
        await call.message.edit_text(text="\u2705 Вы записаны на "
                                          "\n{} \U000027A1\U0000FE0F: {}".format(text_delivery,
                                                                                 transfer_date.split("_")[0]),
                                     reply_markup=await kb_gtc_after_add_date())

    except TypeError:
        dateAdd = query_basket.get_date_added_nurse_by_city(city)

        try:
            async def kb_gtc_add_date():
                kb_gtc_date = InlineKeyboardBuilder()
                collection_date = []
                for i, (date, done, city_i, delivery) in enumerate(dateAdd, start=1):
                    if delivery in "самообращение" and done == "\U0001F4CC":
                        collection_date.append(date.split(' ')[0])
                        # keyboard_gtm.button(text=f"{date.split('_')[0]} {done}", callback_data=f"unique_{date}")

                unique_date = list(set(collection_date))

                for date_i in unique_date:
                    kb_gtc_date.button(text=date_i, callback_data=f"gtcAddDate_{date_i}")
                kb_gtc_date.button(text="назад \U000023EA", callback_data="exit_or_self_conversion")
                kb_gtc_date.adjust(1)
                return kb_gtc_date.as_markup()

            await call.message.edit_text(text=f"<b>Самообращение \U0001F3E5</b>"
                                              f"\nВыберите дату \U00002935\U0000FE0F",
                                         reply_markup=await kb_gtc_add_date())
        except TypeError:
            keyboard_gtm = InlineKeyboardBuilder()
            keyboard_gtm.button(text="назад \U000023EA", callback_data="exit_or_self_conversion")
            keyboard_gtm.adjust(1)
            await call.message.answer(text=f"Свободных дат нет", reply_markup=keyboard_gtm.as_markup())


#  обработка функции для вывода пользователям времени выбранной даты при САМООБРАЩЕНИИ
@router.callback_query(lambda c: c.data.startswith("gtcAddDate_"))
async def process_gtc_time(call: CallbackQuery):
    user_id = call.message.chat.id
    city = query_basket.get_city_basket(user_id)
    input_date = call.data.split('gtcAddDate_')[1]

    dateAdd = query_basket.get_date_added_nurse_by_city(city)

    async def kb_gtc_add_time():
        kb_builder = InlineKeyboardBuilder()
        for p, (date, done, city_i, delivery) in enumerate(dateAdd, start=1):
            if delivery in "самообращение" and done in "\U0001F4CC":
                if input_date in date:
                    kb_builder.button(text=f"{(date.split('_')[0]).split(' ')[1]} {done}",
                                      callback_data=f"unique_{date}")
        kb_builder.adjust(1)
        kb_builder.button(text="назад \U000023EA", callback_data="go_to_medical")
        return kb_builder.as_markup()

    await call.message.edit_text(text=f"<b>Самообращение \U0001F3E5</b>"
                                      f"\nВыберите время \U00002935\U0000FE0F",
                                 reply_markup=await kb_gtc_add_time())


# ==========================================================================================================


# ==========================================================================================================
# 8.0  КОРЗИНА
#   8.1. КОМУ ЗАКАЗАТЬ?
#           8.1.1 = > КНОПКА "МНЕ"
#           8.1.2 = > КНОПКА ДЕТЯМ
# ==========================================================================================================

@router.callback_query(lambda c: c.data == "who_will_order")
async def process_who_will_order(call: CallbackQuery):
    user_id = call.message.chat.id

    await call.message.edit_text("Кому Вы будете оформлять заявку?",
                                 reply_markup=await inline_choice(user_id))


# ОБРАБОТКА КНОПКИ НАЗАД от ВЫБОРОВ ЛЮДЕЙ В КОРЗИНУ - ОСНОВНОЕ МЕНЮ =====================================


@router.callback_query(lambda c: c.data.startswith("whoWillOrder_"))
async def process_back_to_basket_at_who_will_order(call: CallbackQuery):
    user_id = call.message.chat.id
    global transfer_date

    all_prices_back_to_basket = 0  # собирает сумму всех цен
    messages = []  # коллекция дл получения информации о пользователя которая передается в string
    profile = []  # список для получения информации о заявителе в виде
    sampling = 0  # переменная для получения цены на забор биоматериалов
    out_pay = 0  # переменная для получения цены за выезд на адрес
    admin_phone = ""  # переменная для получения номер телефона для перевода за оплату
    admin_bank = ""  # переменная для наименования банка получателя
    city = "\U0001F3D8"
    comment = ""
    try:
        city = query_user.get_city_users(user_id)
        # условия: если сумма анализа превышает 2500 р, то выезд бесплатный, иначе выезд - 500 р.
        res = query_basket.get_info_job_by_city(city)
        for i, (city_in_db, blood, out, address, phone, bank, all_sale) in enumerate(res, start=1):
            sampling = blood
            out_pay = out
            admin_phone = phone
            admin_bank = bank
    except TypeError as error:
        print(error)
    # Комментарии пользователей ===========================================================
    try:
        comment = query_basket.get_comment_basket(user_id)
        if comment is None:
            comment = "без комментариев..."
    except (TypeError, AttributeError):
        pass
    # ==================================================================================================
    # выводим с БД basket users выбранный способ заявки
    try:
        delivery = query_basket.get_delivery_basket(user_id).upper()
    except (TypeError, AttributeError):
        delivery = "\U0000203CВыберите способ заявки!"

    # ==================================================================================================
    # if isinstance(people_one, int):
    #     await bot.delete_message(chat_id=call.message.chat.id, message_id=people_one)
    # =================================================================================================

    # =================================================================================================
    # вывод из БД списка анализов по порядковому номеру
    try:
        result = query_basket.get_added_analyses(user_id)  # БД список анализов
        # =============================================================================================
        # ==========================ВЫВОД АНАЛИЗОВ=============================
        # итерируем получаемый список заказов
        for i, (id_num, name, price, tube, readiness) in enumerate(result, start=1):
            # Добавляем номер перед каждым сообщением
            message_str = f"{i}.<b>{name.split('(')[0]}</b> - {price} р. {readiness}дн."
            messages.append(message_str)
            all_prices_back_to_basket += price

        # Присоединяем все сообщения в одну строку с помощью '\n'.json
        all_messages = "\n".join(messages)
        # ============================================================================================
        if all_prices_back_to_basket >= 2500 or delivery == "самообращение".upper():
            check_out_at = 0
        else:
            check_out_at = out_pay
        # подключение к БД date_add_db для вывода в консоль выбранную ДАТУ
        try:
            date_end = query_basket.get_added_date(user_id).split("_")[0] + "(-/+ 20 мин.)"
        except TypeError:
            date_end = "выберите дату!"
        # ============================================================================================
        # Выводим из БД пользователя все данные для вывода в консоль и введение в БД корзины
        # (basket.db таблица users)
        user_unique_id = call.data.split("whoWillOrder_")[1]

        db_profile = query_user.users_profile_info(user_id, user_unique_id)
        profile.clear()

        for i, (id_us, fio, birth_date, phone, email, city, address) in enumerate(db_profile, start=1):
            profile_info = f"{i}. {fio}\n{birth_date}\n{phone}\n{email}\n{address}"
            profile.append(profile_info)
            # добавляем в базу данных пользователей КОРЗИНЫ после добавления (КОМУ?)
            # для ВЫВОДА в консоль КОРЗИНЫ

            query_basket.set_info_users_in_basket(fio, birth_date, phone, email, address, city, user_id)
            break
        all_profile = "\n".join(profile)

        # для логики: если, пользователь выбирает самообращение то на консоль выходит адрес пункта
        your_self = ""
        if delivery == "самообращение".upper():
            for i, (city_go, sampling, exit_out, address, phone, bank,
                    all_sale) in enumerate(query_basket.get_info_job(), start=1):
                if city_go == city:
                    your_self = "\n" + address
                    break

        # ================================================================================================
        if city is None:
            city = "\U0001F3D8"
        if len(all_profile) > 10:
            await call.message.edit_text(text=all_messages + "\n<b>===========================</b>"
                                                             f"\n<b>Сумма анализа:</b> {all_prices_back_to_basket} р."
                                                             f"\n<b>Забор биоматериала:</b> {sampling} р."
                                                             f"\n<b>Выезд:</b> {check_out_at} р."
                                                             f"\n<b>Общая сумма:</b> "
                                                             f"{all_prices_back_to_basket + check_out_at + sampling} р."
                                                             f"\n<b>===========================</b>"
                                                             f"\n<b>Кому:</b>"
                                                             f"\n{all_profile}"
                                                             "\n<b>===========================</b>"
                                                             f"\n<b>{delivery}</b>"
                                                             f"\n<b>Дата:</b> {date_end.split('>>')[0]}"
                                                             f"\n<b>===========================</b>"
                                                             f"\n<b>Город</b>: {city} {your_self}"
                                                             f"\n<b>===========================</b>"
                                                             f"\n<b>Комментарии:</b> {comment}"
                                                             f"\n<b>===========================</b>"
                                                             f"\n<b>Оплата: </b>переводом на"
                                                             f"\n\U0000203C{admin_bank}\U0000203C<b>{admin_phone}</b>, "
                                                             f"только после взятия биометариала",
                                         reply_markup=await basket_menu())
        else:
            pass
    except aiogram.exceptions.TelegramNotFound:
        await call.message.answer(text="Корзина пуста!")


# ОБРАБОТКА КНОПКИ ВЫБОРА ВЫЗОВА НА ДОМ ИЛИ САМООБРАЩЕНИЯ =======================================================


@router.callback_query(lambda c: c.data == "exit_or_self_conversion")
async def process_exit_or_self_conversion(call: CallbackQuery):
    user_id = call.message.chat.id

    try:
        city = query_basket.get_city_basket(user_id)

        address = query_basket.get_info_job_by_city(city)

        await call.message.edit_text(text="\u203C\uFE0FПри вызове на дом \U0001F3E0, в выбранную дату, мы "
                                          f"приедем к адресу, указанную в заявке!"
                                          f"\n\u203C\uFE0FПри самообращении, ждем Вас по адресу:"
                                          f"\n{city}, {address}", reply_markup=await delivery_in_basket())
    except TypeError:

        await call.message.answer(text="\u203C\uFE0FПри вызове на дом \U0001F3E0, в выбранную дату, мы "
                                       f"приедем к адресу, указанную в заявке!"
                                       f"\nПо данному населенному пункту логистика не сформирована",
                                  reply_markup=await delivery_in_basket())


# ПРИСВОЕНИЕ ДАТЫ
#
# ==========================================================================================================
@router.callback_query(lambda c: c.data and c.data.startswith('unique_'))
async def process_order_date_with_midwifery(call: CallbackQuery):
    global transfer_date
    user_id = call.message.chat.id

    date = (call.data.split("unique_")[1]).split("_")[0]
    nurse_id = (call.data.split("unique_")[1]).split("_")[1]

    transfer_date = "{}_{}".format(date, nurse_id)

    query_basket.update_id_nurse_in_basket(nurse_id, user_id)

    # добавляем в БД фельдшера выбранную дату со значком "галочка"
    query_basket.update_emoji_in_date_nurse("\U0001F530", date, nurse_id)

    # выбранную дату инициализируем в БД для подтверждения (basket.db, таблица - user_{user_id})
    query_basket.init_new_date_in_basket(user_id, date)

    async def kb_back():
        back = InlineKeyboardBuilder()
        back.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
        back.adjust(1)
        return back.as_markup()

    await call.message.edit_text(text="\U0000203CВыбрано: {}".format(date), reply_markup=await kb_back())


# ==========================================================================================================
# 8.0  КОРЗИНА
#   8.1. КОМУ ЗАКАЗАТЬ?
#           8.1.1 = > КНОПКА "МНЕ" - готово!
#           8.1.2 = > КНОПКА "ВЫБРАТЬ ДАТУ ЗАКАЗА"
#           8.1.2.1  => ОБРАБОТКА КНОПКИ ВЫБОРА ЗАКАЗА ПОСЛЕ НАЖАТИЯ
#               8.1.2.1.1 => УДАЛИТЬ ВЫБРАННУЮ ДАТУ
#
# ==========================================================================================================
# показать все даты по вызову на дом ========================================================================
# Дописать то, что при обработки этой callback должны быть внесены изменения в БД
@router.callback_query(lambda c: c.data.startswith("delAddDate"))
async def process_delete_date_in_database(call: CallbackQuery):
    global transfer_date
    user_id = call.message.chat.id
    date = call.data.split("delAddDate")[1]

    # добавляем в БД фельдшера выбранную дату со значком "инструмент"
    query_basket.update_emoji_after_delete_date_in_basket("\U0001F4CC", date)

    query_basket.update_delivery_in_basket(None, user_id)

    query_basket.delete_date_in_basket(user_id)

    async def kb_back():
        back = InlineKeyboardBuilder()
        back.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
        back.adjust(1)
        return back.as_markup()

    await call.message.edit_text(text="Удалено!", reply_markup=await kb_back())


# =========================== ШАБЛОНЫ =================================================================
@router.callback_query(lambda c: c.data == "pattern")
async def process_pattern(call: CallbackQuery):
    user_id = call.message.chat.id

    await call.message.edit_text(text="\U0001F39E Список шаблонов: ", reply_markup=await kb_patterns(user_id))


@router.callback_query(lambda c: c.data and c.data.startswith("pat_"))
async def process_pattern_found(call: CallbackQuery):
    user_id = call.message.chat.id

    pattern_found = call.data.split('pat_')[1]
    # выводим из БД шаблонов цифры полученные из наименования
    id_numbers = query_basket.get_numbers_pattern(user_id, pattern_found)
    # переводим id_numbers в список
    selected = [item.strip() for item in id_numbers.split(",")]
    # получаем все данные из БД анализов
    all_analyses = query_search_analyses.all_analyses()
    # переменная для получения суммы цен всех анализов из БД
    summ_text_pattern = 0
    # список для получения текста содержащее имени, цену и срок готовности анализа в шаблоне
    collection_text_pattern = []
    count = 1
    # итерируем БД анализов и ищем из него анализы в шаблоне
    for i, (id_num, id_list, name_analysis, price, info, tube, readiness, sale, sale_num,
            price_other, stopped) in enumerate(all_analyses, start=1):
        if id_num in map(int, selected):
            text_pattern = f"{count}. {name_analysis}: {price} \u20BD Срок: {readiness} дн."
            collection_text_pattern.append(text_pattern)
            summ_text_pattern += price
            count += 1
    text_pattern_all = "\n".join(collection_text_pattern)

    # создаем кнопки для добавления, удаления шаблона в корзину и удаления самого шаблона

    async def kb_pattern_inline():
        kb_info_pattern = InlineKeyboardBuilder()
        kb_info_pattern.button(text="выбрать \u267B", callback_data=f"add_pattern_{pattern_found}")
        kb_info_pattern.button(text="удалить из корзины \U0001F4A2",
                               callback_data=f"clear_pattern_in_basket_{pattern_found}")
        kb_info_pattern.button(text="удалить шаблон \U0001F5D1", callback_data=f"delete_pattern_in_db_{pattern_found}")
        kb_info_pattern.button(text="назад \U000023EA", callback_data="pattern")
        kb_info_pattern.adjust(2)
        return kb_info_pattern.as_markup()

    await call.message.edit_text(text=text_pattern_all + "\n========================="
                                                         f"\nОбщая сумма: {summ_text_pattern} \u20BD"
                                                         f"\n=========================",
                                 reply_markup=await kb_pattern_inline())


# ================ ДОБАВИТЬ ШАБЛОН ========================================================================
@router.callback_query(lambda c: c.data.startswith("add_pattern_"))
async def process_pattern_found(call: CallbackQuery):
    user_id = call.message.chat.id

    pattern_found = call.data.split('add_pattern_')[1]

    id_numbers = query_basket.get_numbers_pattern(pattern_found, user_id)

    for i, (id_num, id_list, name_analysis, price, info, tube, readiness, sale, sale_num,
            price_other, stopped) in enumerate(query_search_analyses.all_analyses(), start=1):
        if str(id_num) in id_numbers:
            price_income = price - price_other
            query_search_analyses.add_analyses(user_id, id_list, name_analysis, price, tube, readiness, price_other,
                                               price_income)

    async def kb_pattern_inline():
        kb_info_pattern = InlineKeyboardBuilder()
        kb_info_pattern.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
        kb_info_pattern.adjust(1)
        return kb_info_pattern.as_markup()

    await call.message.edit_text(text=f"Список анализов добавлен в корзину!",
                                 reply_markup=await kb_pattern_inline())


# ================ УДАЛИТЬ ШАБЛОН В КОРЗИНЕ  =====================================================================
@router.callback_query(lambda c: c.data and c.data.startswith("clear_pattern_in_basket_"))
async def process_pattern_found_delete_in_basket(call: CallbackQuery):
    user_id = call.message.chat.id

    pattern_found = call.data.split('clear_pattern_in_basket_')[1]

    id_numbers = query_basket.get_numbers_pattern(pattern_found, user_id)

    res = query_basket.get_added_analyses(user_id)

    for i, (id_num, name_analysis, price, tube, readiness) in enumerate(res, start=1):
        if str(id_num) in id_numbers:
            query_search_analyses.delete_analyses_in_db(user_id, id_num)

    async def kb_pattern_inline():
        kb_info_pattern = InlineKeyboardBuilder()
        kb_info_pattern.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
        kb_info_pattern.adjust(1)
        return kb_info_pattern.as_markup()

    await call.message.edit_text(text=f"Удален из КОРЗИНЫ!", reply_markup=await kb_pattern_inline())


# ================ УДАЛИТЬ ШАБЛОН В БД  ===================================================================
@router.callback_query(lambda c: c.data and c.data.startswith("delete_pattern_in_db_"))
async def process_pattern_found_delete_in_db(call: CallbackQuery):
    user_id = call.message.chat.id
    pattern_delete_name = call.data.split("delete_pattern_in_db_")[1]

    query_basket.delete_pattern(user_id, pattern_delete_name)

    async def kb_pattern_delete():
        kb_del_pattern = InlineKeyboardBuilder()
        kb_del_pattern.button(text="назад \U000023EA", callback_data="pattern")
        kb_del_pattern.adjust(1)
        return kb_del_pattern.as_markup()

    await call.message.edit_text(text=f"Шаблон удалён! ",
                                 reply_markup=await kb_pattern_delete())


# ==========================================================================================================
# 8.0  КОРЗИНА
#   8.1 = > КОМУ ЗАКАЗАТЬ?
#           8.1.1 = > КНОПКА "МНЕ" - готово!
#   8.2 = > КНОПКА "ВЫБРАТЬ ДАТУ ЗАКАЗА"
#           8.1.32 = > КНОПКА "НАЗАД В КОРЗИНУ" - готово!
#           8.1.33 = > КНОПКА "СЛЕДУЮЩИЙ МЕСЯЦ"
#                8.1.33.1 = > КНОПКА "НАЗАД" в предыдущий месяц - готово!
#
#   8.4 = > РЕДАКТИРОВАТЬ ЗАКАЗ = > Редактировать СПИСОК
#
# ==========================================================================================================

@router.callback_query(lambda c: c.data == "edit_list_order")
async def process_edit_basket_analyses_menu(call: CallbackQuery):
    user_id = call.message.chat.id
    messages = []

    # выводим с БД basket.db таблицы basket_list список выбранных анализов
    result = query_basket.get_added_analyses(user_id)
    # итерируем получаемый список заказов
    for i, (id_num, name, price, tube, readiness) in enumerate(result, start=1):
        # Добавляем номер перед каждым сообщением
        message_str = f"{i}. <b>код {id_num}</b>: {name.split('(')[0]}"
        messages.append(message_str)

    # Присоединяем все сообщения в одну строку с помощью '\n'
    all_messages = "\n".join(messages)

    async def kb_edit_list_analyses():
        kb_edit_analyses = InlineKeyboardBuilder()
        kb_edit_analyses.button(text="Изменить список \U0001F4D6", callback_data="edit_analyses_list")
        kb_edit_analyses.button(text="Удалить весь список \U00002702 \U0000FE0F", callback_data="delete_analyses_list")
        kb_edit_analyses.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
        kb_edit_analyses.adjust(1)
        return kb_edit_analyses.as_markup()

    await call.message.edit_text(text=all_messages + "\n==========================="
                                                     "\nРедактировать список анализов: ",
                                 reply_markup=await kb_edit_list_analyses())


# ==========================================================================================================
# 8.0  КОРЗИНА
#   8.1 = > КОМУ ЗАКАЗАТЬ?
#           8.1.1 = > КНОПКА "МНЕ" - готово!
#   8.2 = > КНОПКА "ВЫБРАТЬ ДАТУ ЗАКАЗА"
#           8.1.32 = > КНОПКА "НАЗАД В КОРЗИНУ" - готово!
#           8.1.33 = > КНОПКА "СЛЕДУЮЩИЙ МЕСЯЦ"
#                8.1.33.1 = > КНОПКА "НАЗАД" в предыдущий месяц - готово!
#   8.3 = > ОПЛАТИТЬ ЗАКАЗ
#   8.4 = > РЕДАКТИРОВАТЬ ЗАКАЗ = > Редактировать СПИСОК
#       8.4.1 = > РЕДАКТИРОВАТЬ СПИСОК АНАЛИЗОВ УДАЛЯЯ ПО ОДНОМУ АНАЛИЗУ
#
# ==========================================================================================================

@router.callback_query(lambda c: c.data == "edit_analyses_list")
async def process_edit_list_order(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='\U0001F522 Введите КОД-анализа, которого хотите удалить:')

    await state.set_state(States.waiting_for_edit_list_order)


# ==========================ОБРАБОТКА КНОПКИ УДАЛЕНИЕ АНАЛИЗА ИЗ КОРЗИНЫ=======
@router.message(States.waiting_for_edit_list_order)
async def process_edit_list_order_done(message: Message, state: FSMContext):
    key = message.text
    user_id = message.chat.id

    name = query_basket.get_name_analyses_in_list_basket(user_id, key)

    query_basket.delete_analyses_in_list_basket(user_id, key)

    keyb = InlineKeyboardBuilder()
    keyb.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
    keyb.adjust(1)
    await message.answer(text=f"<b>{key}: {name}</b> => Удален!",
                         reply_markup=keyb.as_markup())
    await state.clear()


# ==========================================================================================================
# 8.0  КОРЗИНА
#   8.1 = > КОМУ ЗАКАЗАТЬ?
#           8.1.1 = > КНОПКА "МНЕ" - готово!
#   8.2 = > КНОПКА "ВЫБРАТЬ ДАТУ ЗАКАЗА"
#           8.1.32 = > КНОПКА "НАЗАД В КОРЗИНУ" - готово!
#           8.1.33 = > КНОПКА "СЛЕДУЮЩИЙ МЕСЯЦ"
#                8.1.33.1 = > КНОПКА "НАЗАД" в предыдущий месяц - готово!
#   8.3 = > ОПЛАТИТЬ ЗАКАЗ
#   8.4 = > РЕДАКТИРОВАТЬ ЗАКАЗ = > Редактировать СПИСОК
#       8.4.1 = > РЕДАКТИРОВАТЬ СПИСКО АНАЛИЗОВ УДАЛЯЯ ПО ОДНОМУ АНАЛИЗУ
#       8.4.2 = > УДАЛИТЬ ВЕСЬ СПИСОК АНАЛИЗОВ
# ==========================================================================================================
@router.callback_query(lambda c: c.data == "delete_analyses_list")
async def process_edit_basket_analyses_menu(call: CallbackQuery):
    user_id = call.message.chat.id

    query_basket.delete_all_analyses(user_id)

    query_basket.delete_all_analyses_in_profit(user_id)

    async def delete_list_analyses():
        keyb = InlineKeyboardBuilder()
        keyb.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
        keyb.adjust(1)
        return keyb.as_markup()

    await call.message.edit_text(text="Удален весь список анализов!",
                                 reply_markup=await delete_list_analyses())


# КОММЕНТАРИИ К ЗАЯВКЕ ==========================================================================================
@router.callback_query(lambda c: c.data == "comment")
async def process_comment_basket(call: CallbackQuery):
    async def kb_info_comment():
        keyb_comment = InlineKeyboardBuilder()
        keyb_comment.button(text="оставить комментарии", callback_data="add_comment")
        keyb_comment.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
        keyb_comment.adjust(1)
        return keyb_comment.as_markup()

    await call.message.edit_text(text="\U00002757 С целью уточнений о заявке и анализах можете оставить "
                                      "комментарии мед.персоналу."
                                      "\n\U00002757Также если, хотите оставить заявку на еще одного человека, "
                                      "то допишите данные в комментарии по образцу!"
                                      "\n1. ФИО:"
                                      "\n2. Дата рождения:"
                                      "\n3. Анализы:",
                                 reply_markup=await kb_info_comment())


@router.callback_query(lambda c: c.data == "add_comment")
async def process_add_comment_basket(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.waiting_for_add_comment)
    await call.message.edit_text(text='Введите текст комментарии: ')


# ==========================ОБРАБОТКА СТАТУСА "НАЗАД" ПОСЛЕ РЕДАКТИРОВАНИЯ ФАМИЛИИ 3-ГО РЕБЕНКА==========
@router.message(States.waiting_for_add_comment)
async def process_edit_female_three_done(message: Message, state: FSMContext):
    comment = message.text

    query_basket.update_new_comment_in_basket(comment, message.chat.id)

    keyb_back = InlineKeyboardBuilder()
    keyb_back.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
    keyb_back.adjust(1)

    await message.answer(text="\U0001F4DD")
    await message.answer(text='Сохранено!', reply_markup=keyb_back.as_markup())
    await state.clear()


# ================================================================================================================
#                                               ПОДТВЕРЖДЕНИЕ ЗАЯВКИ
# ================================================================================================================

@router.callback_query(lambda c: c.data == "confirm_the_order")
async def process_confirm_the_order(call: CallbackQuery):
    user_id = call.message.chat.id

    query_basket.create_new_table_orders(user_id)

    async def kb_confirm():
        kb_conf = InlineKeyboardBuilder()
        kb_conf.button(text="Подтвердить заявку \U0000267B \U0000FE0F", callback_data="confirm_button")
        kb_conf.button(text="назад \U000023EA", callback_data="back_to_basket_menu")
        kb_conf.adjust(1)
        return kb_conf.as_markup()

    await call.message.edit_text(
        text="1. После подтверждения заявки, невозможно его отредактировать!"
             "\n2. Все данные с КОРЗИНЫ исчезнут!"
             "\n3. Проверьте личные данные, список "
             "анализов и общую сумму оплаты!", reply_markup=await kb_confirm())


# =================================================================================================================
#                                     обработка кнопки ПОДТВЕРЖДЕНИЯ
# =================================================================================================================

@router.callback_query(lambda c: c.data == "confirm_button")
async def process_confirm_basket(call: CallbackQuery):
    user_id = call.message.chat.id

    # ===================================================================================================
    message_name = ""  # переменная для получения ФИО (и других данных) выбранного человек
    tube_for_midwifary = []  # переменная для получения значения
    collection_analysis = []  # переменная для получения каждого анализа
    collection_analysis_all = []  # коллекция добавляет только наименование анализов и передает в БД медсестрам
    fio_by_dir = ""
    prices = 0
    id_midwiferys = ""
    delivery = ""
    user_address = ""  # передаем адрес для медсестер
    comment = ""

    # ===================================================================================================
    async def kb_back_to_basket():
        kb_confirm_back = InlineKeyboardBuilder()
        kb_confirm_back.button(text="назад ", callback_data="back_to_basket_menu")
        kb_confirm_back.adjust(1)
        return kb_confirm_back.as_markup()

    # ===================================================================================================

    # =========================РАБОТА С БАЗОЙ ДАННЫХ ВЫБРАННЫХ ЗНАЧЕНИЙ==================================
    #  _1 вытаскиваем с БД все выбранные анализы
    res = query_basket.get_added_analyses(user_id)

    for i, (id_code, name_analysis, price, tube, readiness) in enumerate(res, start=1):
        message_analysis = f"{id_code}>>{name_analysis}: {price} р., срок: {readiness} дн."
        analyses_add = f"{id_code}>>{name_analysis};"
        collection_analysis.append(message_analysis)
        collection_analysis_all.append(analyses_add)
        if id_code < 483:
            tube_for_midwifary.append(f"1шт - {tube}")
        else:
            tube_for_midwifary.append(f"1шт - {tube}")

        prices += price

    list_analysis = list(set(collection_analysis))
    tube_collection = list(set(tube_for_midwifary))
    tube = "\n".join(tube_collection)
    analysis_all = "\n".join(list_analysis)
    analysis_by_order_done = ", ".join(collection_analysis_all)

    # ОБРАЗОВАНИЕ ОБЩЕЙ СУММЫ АНАЛИЗОВ ========================================================================
    city_in_db_basket_add = query_basket.get_city_basket(user_id)
    sampling = 0
    out_pay = 0
    for i, (city_in_db_services, blood, out, street, phone, bank,
            all_sale) in enumerate(query_basket.get_info_job(), start=1):
        if city_in_db_services == city_in_db_basket_add:
            sampling = blood
            out_pay = out

    out_dor = query_basket.get_delivery_basket(user_id)
    if prices + sampling >= 2500 or out_dor == "самообращение":
        prices += sampling
    else:
        prices += out_pay + sampling

    # ========================================================================================================

    # _2 вытаскиваем с БД basket выбранного человека и добавляем в БД basket в таблицу user_{user_id}
    result_name = query_basket.get_info_users_in_basket(user_id)

    # _3 вытаскиваем дату и сравниваем есть ли такая дата в БД
    try:
        result_date = query_basket.get_added_date(user_id).split("_")[0]

        # _5 вытаскиваем с БД basket выбранного человека и добавляем в БД basket в таблицу user_{user_id}
        for i, (user, fio, birth, phone, email, address, city_in_db_basket_users,
                deliver, comm, id_mid) in enumerate(result_name, start=1):
            message_name = f"{fio}, {birth}г.\n{phone}\n{email}."
            user_address = address
            fio_by_dir = f"{fio}."
            delivery = deliver
            id_midwiferys = id_mid
            if comm is None:
                comment = "без комментариев..."
            else:
                comment = comm
            break

    except TypeError:
        result_date = "Выберите дату!"

    # =========================================================================================================
    if len(analysis_all) < 10:
        await call.message.edit_text(text="\U0001F449 Выберите анализы!", reply_markup=await kb_back_to_basket())
    elif result_name[0][1] is None:
        await call.message.edit_text(text="\U0001F449 Выберите заказчика!", reply_markup=await kb_back_to_basket())
    elif result_date == "Выберите дату!":
        await call.message.edit_text(text="\U0001F449 Выберите дату!", reply_markup=await kb_back_to_basket())
    else:

        # ===================================================================================================
        # ===================================================================================================
        # переносим все выбранные анализы из profit.db в БД profit_income.db
        string_collection = []
        price_all_other_analyses = 0
        profit = query_basket.get_info_profit(user_id)
        for i, (id_list, name_analysis, price, price_other, price_income) in enumerate(profit, start=1):
            long_string = (f"*** {id_list}: {name_analysis} \n---- цена: {price} р. "
                           f"стоимость: {price_other} р. кэш: {price_income}")
            string_collection.append(long_string)
            price_all_other_analyses += int(price_other)
        string_long_info = "\n".join(string_collection)

        # ====================================================================================
        # инициализируем в БД админа данные о заказе, и прибыли
        price_all_income = prices - price_all_other_analyses

        query_basket.init_new_profit_income(result_date, fio_by_dir, string_long_info, prices, price_all_other_analyses,
                                            price_all_income)

        # ====================================================================================
        # удаляем БД таблицу пользователя profit.db
        query_basket.delete_all_analyses_in_profit(user_id)
        # ====================================================================================
        # добавляем в БД basket в таблицу user_{user_id}

        city = query_basket.get_city_basket(user_id)

        query_basket.init_new_orders_in_basket(user_id, result_date, message_name, analysis_all, user_address, prices,
                                               city, delivery, comment, id_midwiferys)
        # ====================================================================================

        # ================================================================================================
        # в БД фельдшера, где будет выводить готовую заявку

        query_basket.init_new_order_nurse(id_midwiferys, result_date, message_name, analysis_by_order_done, tube, city,
                                          delivery, user_address, comment, "не выполнено",
                                          "не подтверждена", user_id, prices, price_all_other_analyses,
                                          price_all_income)

        # ===================================================================================================
        # =======================           УДАЛЕНИЕ           ==============================================
        # ===================================================================================================

        # удаляем выбранного пользователя с корзины
        query_basket.delete_user_in_basket(user_id)
        # ===================================================================================================
        # удаляем список выбранных анализов с корзины
        query_basket.delete_all_analyses(user_id)
        # ===================================================================================================
        # ===================================================================================================
        # удаляем ДАТУ с нашей БД (date_person.db)
        query_basket.delete_date_in_basket(user_id)

        # добавляем в БД фельдшера выбранную дату со значком "галочка"
        query_basket.update_emoji_in_date_nurse("\U0001F4C6", result_date, id_midwiferys)


        count = 4
        text = "  " * count
        message_id = await call.message.edit_text("Формируется заявка" + text)
        for i in range(count):
            text = text.replace(" ", ".", 1)
            await call.message.bot.edit_message_text(text="Формируется заявка" + text,
                                                     chat_id=call.message.chat.id,
                                                     message_id=message_id.message_id)
            await asyncio.sleep(1)

        await call.answer("Заявка успешно оформлена! "
                          "\nВаши данные переданы в ЗАЯВКИ \U000027A1"
                          "\nСписок заявок закреплена значком \U0000274C, "
                          "\nПри подтверждении заявки медсестрой "
                          "\nзначок сменится на \u2705", show_alert=True)
        await call.message.answer(text="\U0001F389")
        await call.message.answer_photo(
            photo="https://cdn.pixabay.com/photo/2024/03/06/16/38/application-8616753_1280.jpg",
            caption="Переходите в заявки")
