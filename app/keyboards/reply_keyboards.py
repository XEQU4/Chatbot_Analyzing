from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class RKB:
    """
    Class with reply keyboard functions
    """

    @staticmethod
    async def contact() -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📱 Отправить контакт", request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        return keyboard