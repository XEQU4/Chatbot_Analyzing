from aiogram import Router
from aiogram import exceptions
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent

from asyncpg import PostgresError

from app.logger import logger

router = Router()


@router.error(ExceptionTypeFilter(exceptions.CallbackAnswerException))
async def error_handler1(event: ErrorEvent):
    logger.warning(f"\n\taiogram error: CallbackAnswerException - Исключение для ответа на обратный вызов\n\tevent error: {event.exception}\n\n\tCallback: {event.update.callback_query}\n\tUpdate: {event.update}\n")

    raise event.exception


@router.error(ExceptionTypeFilter(exceptions.TelegramNotFound))
async def error_handler2(event: ErrorEvent):
    logger.warning(f"\n\taiogram error: TelegramNotFound - Чат / Пользователь / Сообщение не найдено\n\tevent error: {event.exception}\n\n\tMessage: {event.update.message}\n\tUpdate: {event.update}\n")

    raise event.exception


@router.error(ExceptionTypeFilter(exceptions.TelegramRetryAfter))
async def error_handle3r(event: ErrorEvent):
    logger.warning(f"\n\taiogram error: TelegramRetryAfter - Слишком высокая интенсивность отправки сообщении, надо подождать - {str(event.exception).split()[-7]} сек.\n\tevent error: {event.exception}\n\n\tMessage: {event.update.message}\n\tUpdate: {event.update}\n")

    raise event.exception


@router.error(ExceptionTypeFilter(exceptions.TelegramBadRequest))
async def error_handler4(event: ErrorEvent):
    logger.warning(f"\n\taiogram error: TelegramBadRequest - Неверный запрос\n\tevent error: {event.exception}\n\n\tMessage: {event.update.message}\n\tUpdate: {event.update}\n")

    raise event.exception


@router.error(ExceptionTypeFilter(exceptions.TelegramUnauthorizedError))
async def error_handler5(event: ErrorEvent):
    logger.error(f"\n\taiogram error: TelegramUnauthorizedError - Токен бота стал не действителен\n\tevent error: {event.exception}\n\n\tUpdate: {event.update}\n")


@router.error(ExceptionTypeFilter(exceptions.TelegramForbiddenError))
async def error_handler6(event: ErrorEvent):
    logger.warning(f"\n\taiogram error: TelegramForbiddenError - Бота исключили из чата\n\tevent error: {event.exception}\n\n\tUpdate: {event.update}\n")

    raise event.exception


@router.error(ExceptionTypeFilter(PostgresError))
async def error_handler7(event: ErrorEvent):
    logger.warning(f"\n\tasyncpg error: PostgresError\n\tevent error: {event.exception}\n\n\tUpdate: {event.update}\n")

    raise event.exception


@router.error()
async def error_handler(event: ErrorEvent):
    logger.error(f"\n\taiogram error: Неизвестная ошибка\n\tevent error: {event.exception}\n\n\tUpdate: {event.update}\n")

    raise event.exception
