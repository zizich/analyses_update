from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    waiting_for_add_comment = State()
    waiting_for_save_pattern_name = State()
    waiting_for_search_after_confirm = State()
    waiting_for_search_before_confirm = State()
    waiting_for_search = State()
    waiting_for_edit_list_order = State()
    # ================================================
    waiting_for_general_clinic = State()
    waiting_for_add_name_people_one = State()
    waiting_for_add_female_people_one = State()
    waiting_for_add_patronymic_people_one = State()
    waiting_for_add_birth_date_people_one = State()
    waiting_for_add_phone_people_one = State()
    waiting_for_add_email_people_one = State()
    waiting_for_add_address_people_one = State()
    waiting_for_add_fio_people_one = State()
    waiting_for_edit_female_people_one = State()
    waiting_for_edit_patronymic_people_one = State()
    waiting_for_edit_birth_date_people_one = State()
    waiting_for_edit_phone_people_one = State()
    waiting_for_edit_email_people_one = State()
    waiting_for_edit_address_people_one = State()
    # =================================================
    waiting_for_others_one = State()
    waiting_for_others_two = State()
    waiting_for_others_three = State()
    # =================================================
    waiting_for_add_four_child_name = State()
    waiting_for_add_four_child_female = State()
    waiting_for_add_four_child_patronymic = State()
    waiting_for_add_four_child_birth_date = State()
    waiting_for_edit_four_child_name = State()
    waiting_for_edit_four_child_female = State()
    waiting_for_edit_four_child_patronymic = State()
    waiting_for_edit_four_child_birth_date = State()
    # ===================================================
    waiting_for_add_three_child_name = State()
    waiting_for_add_three_child_female = State()
    waiting_for_add_three_child_patronymic = State()
    waiting_for_add_three_child_birth_date = State()
    waiting_for_edit_three_child_name = State()
    waiting_for_edit_three_child_female = State()
    waiting_for_edit_three_child_patronymic = State()
    waiting_for_edit_three_child_birth_date = State()
    # ===================================================
    waiting_for_add_two_child_name = State()
    waiting_for_add_two_child_female = State()
    waiting_for_add_two_child_patronymic = State()
    waiting_for_add_two_child_birth_date = State()
    waiting_for_edit_two_child_name = State()
    waiting_for_edit_two_child_female = State()
    waiting_for_edit_two_child_patronymic = State()
    waiting_for_edit_two_child_birth_date = State()
    # ====================================================
    waiting_for_edit_child_name_one = State()
    waiting_for_edit_child_female_one = State()
    waiting_for_edit_child_patronymic_one = State()
    waiting_for_edit_child_birth_day_one = State()
    waiting_for_add_child_birth_date = State()
    waiting_for_add_child_patronymic_button = State()
    waiting_for_add_child_female_button = State()
    waiting_for_add_child_button = State()
    # ====================================================
    waiting_for_edit_address_user = State()
    waiting_for_edit_email_user = State()
    waiting_for_edit_phone_user = State()
    waiting_for_edit_birth_date_user = State()
    waiting_for_edit_patronymic_user = State()
    waiting_for_edit_female_user = State()
    waiting_for_edit_fio_user = State()
    waiting_for_fio = State()
    waiting_for_female = State()
    waiting_for_patronymic = State()
    waiting_for_birth_day = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_address = State()
    waiting_for_reply_menu = State()
    # ====================================================
    CHOOSING_SPEC = State()
    CHOOSING_COURSE = State()
    CHOOSING_TYPE = State()
    TYPING = State()
