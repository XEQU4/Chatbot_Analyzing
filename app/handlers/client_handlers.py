import contextlib

from aiogram import Router, exceptions
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart

from app.keyboards import IKB, RKB
from app.config import config
from app.fsm import FSM
from app.database import get_statistics_text_from_db
from app.dispatcher import bot

router = Router()


@router.callback_query(FSM.query_waiting, lambda query: query.data == "start")
async def query_start(query: CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=None)

    text = ("Вопрос: Есть ли вам 23 года?\n"
            "Напишите ⬇️")
    await query.message.answer(text=text)

    await state.set_state(FSM.first_answer_waiting)


@router.callback_query(lambda query: query.data == "statistics")
async def query_start(query: CallbackQuery):
    text = await get_statistics_text_from_db()
    await query.message.answer(text=text,
                               parse_mode=ParseMode.HTML)


@router.message(lambda message: message.text is not None, FSM.first_answer_waiting)
async def first_answer(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer(text="Ну вы чего, введите буквы, цифры, да хоть иероглифы, но не картинки и другие медиа 👀")
        return

    await state.update_data(first=message.text)

    text = "Вопрос: Вы проживаете в Москве или в Московской области?"
    await message.answer(text=text)

    await state.set_state(FSM.second_answer_waiting)


@router.message(lambda message: message.text is not None, FSM.second_answer_waiting)
async def second_answer(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer(text="Ну вы чего, введите буквы, цифры, да хоть иероглифы, но не картинки и другие медиа 👀")
        return

    await state.update_data(second=message.text)

    text = "Вопрос: Имеется ли у вас юридическое лицо?"
    await message.answer(text=text)

    await state.set_state(FSM.third_answer_waiting)


@router.message(lambda message: message.text is not None, FSM.third_answer_waiting)
async def third_answer(message: Message, state: FSMContext):
    await state.update_data(third=message.text)

    text = "Чтобы специалисты могли с вами связаться, поделитесь контактом ⬇️"
    await message.answer(text=text,
                         reply_markup=await RKB.contact())

    await state.set_state(FSM.contact_waiting)


@router.message(lambda message: message.contact is not None, FSM.contact_waiting)
async def handle_contact(message: Message, state: FSMContext):
    text = "Спасибо за прохождение анкеты! Специалист свяжется с вами в ближайшее время"
    await message.answer(text=text)

    state_data = await state.get_data()
    if message.chat.id not in config.admins_ids:
        await state.set_state(FSM.passed)
        await config.set_views(full_form=True)
        await state.update_data(passed=True)
    else:
        await state.clear()

    text = (f"Пользователь прошел анкету:\n"
            f"    Вопрос: Есть ли вам 23 года?\n"
            f"    Напишите ⬇️\n"
            f"    Ответ: {state_data['first']}\n\n"
            f"    Вопрос: Вы проживаете в Москве или в Московской области?\n"
            f"    Ответ: {state_data['second']}\n\n"
            f"    Вопрос: Имеется ли у вас юридическое лицо?\n"
            f"    Ответ: {state_data['third']}\n\n"
            f"Немного данных пользователя:\n"
            f"    Имя аккаунта телеграмм: {message.chat.first_name if message.chat.first_name is not None else ''} "
            f"{message.chat.last_name if message.chat.last_name is not None else ''}\n"
            f"    Имя пользователя (@username): {message.chat.username if message.chat.username else 'Нету'}\n"
            f"    Телефон номера: {message.contact.phone_number}")
    for admin_id in config.admins_ids:
        with contextlib.suppress(exceptions.TelegramForbiddenError, exceptions.TelegramBadRequest):
            await bot.send_message(chat_id=admin_id,
                                   text=text,
                                   reply_markup=await IKB.url_to_user(message.from_user.url))


@router.message()
@router.message(CommandStart)
async def command_start_handling(message: Message, state: FSMContext):
    if message.chat.id in config.admins_ids:
        await state.clear()
    else:
        state_data = await state.get_data()
        if state_data.get('passed', False):
            await message.answer(text="Вы же уже прошли анкету 😁")
            return
        if not state_data.get('started', False):
            await config.set_views(views=True)
            await state.update_data(started=True)
        await state.update_data(passed=False)

    await state.update_data(first="")
    await state.update_data(second="")
    await state.update_data(third="")

    text, image_path = await config.get_text_img()
    if image_path is not None:
        photo = FSInputFile(image_path)
        await message.answer_photo(caption=text,
                                   photo=photo,
                                   reply_markup=await IKB.start(is_admin=(message.chat.id in config.admins_ids)),
                                   parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await message.answer(text=text,
                             reply_markup=await IKB.start(is_admin=(message.chat.id in config.admins_ids)),
                             parse_mode=ParseMode.MARKDOWN_V2)

    await state.set_state(FSM.query_waiting)