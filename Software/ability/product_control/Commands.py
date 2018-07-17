#!/usr/bin/env python
class COMMANDS:
    def __init__(self):
        pass

    # login
    WIFI_CONNECT = "wifi_connect"
    WIFI_LISTS = 'wifi_lists'
    CHECK_WIFI = "wifi_has_internet"
    WIFI_CURRENT_NAME = "wifi_current_name"

    CHECK_WIFI_FOR_PHONE = "check_wifi"

    GET_QR_IMAGE = "get_qr_image"

    LIST_TASKS = "list_tasks"
    LIST_TASKS_PA = "list_tasks_pa"

    CHECK_PRODUCT = "check_product"

    DOWNLOAD_ABILITY = "download_ability"

    USER_ALL_ABILITY = "user_all_ability"

    USER_ADD_ABILITY = "user_add_ability"
    USER_UPDATE_ABILITY = "user_update_ability"
    USER_REMOVE_ABILITY = "user_remove_ability"

    CHECK_OUT = "user_check_out"

    PHONE_CHECK_OUT = "phone_check_out"

    PHONE_CHECK_IN = "phone_check_in"

    CHECK_IN = "user_check_in"

    USER_ADD_TASK = "user_add_task"

    USER_EDIT_TASK = "user_edit_task"

    USER_UPDATE_INFO = "user_update_info"

    USER_REMOVE_GROUP_VARIABLE_VALUE = "user_remove_group_variable_value"
    USER_SET_DEFAULT_GROUP_VARIABLE_VALUE = "user_set_default_group_variable_value"

    FIRMWARE_UPDATE = 'update_firmware'

    NEW_FIRMWARE = "new_firmware"

    CHECK_INTERNET_CONNECTION = "check_internet_connection"
    START_CHECK_INTERNET_CONNECTION = "start_check_internet_connection"
    STOP_CHECK_UPDATE = "stop_check_update"
    CONTINUE_CHECK_UPDATE = "continue_check_update"

    # DESK CONTROL ACTION:

    CHECK_VERSION = "check_version"

    SAVE_DESK_ADDRESS = "save_desk_address"

    READY_IN_USE = "ready_in_use"

    CURRENT_SETTINGS = "current_settings"
    CHECK_OUT_CONFIRM = "user_check_out_confirm"

    CONFIRM_RESTART_OS = "confirm_restart_os"
    RESTART_OS = "restart_os"

    CARD_INFO = "card_info"
    ADD_CARD = "add_card"
    EDIT_CARD = "edit_card"
    USER_INFO = "user_info"

    # COMMON
    SYNC_USER_INFO = "sync_user_info"
    FACTORY_RESET = "factory_reset"
    UPDATE_WIFI = "update_wifi"
    IP_ADDRESS = 'ip_address'
    EMERGENCY_STOP = 'emergency_stop'
    RESET_ALL = 'reset_all'
    PLATFORM = 'platform'
    ABILITY_VERSION = 'ability_version'
