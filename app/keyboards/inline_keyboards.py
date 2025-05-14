from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class IKB:
    """
    Class with inline keyboard functions
    """

    @staticmethod
    async def start(is_admin: bool = False) -> InlineKeyboardMarkup:
        buttons_rows = [[InlineKeyboardButton(text="📝 Начать", callback_data="start")]]
        if is_admin:
            buttons_rows.append([InlineKeyboardButton(text="📊 Посмотреть статистику", callback_data="statistics")])

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)

    @staticmethod
    async def url_to_user(url) -> InlineKeyboardMarkup:
        buttons_rows = [[InlineKeyboardButton(text="Перейти в профиль", url=url)]]

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)