from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from bot.database.session import get_db
from bot.database.models import Users
from bot.config import ADMIN_IDS
from bot.keyboards.keyboards import gift_sent_button, admin_menu
from bot.states.states import Form

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    db = get_db()
    user = db.query(Users).filter(Users.telegram_id == 
                                  message.from_user.id).first()

    if not user:
        user = Users(
            telegram_id=message.from_user.id,
            is_admin=message.from_user.id in ADMIN_IDS
        )
        db.add(user)
        db.commit()

    if user.name:
        if user.is_admin:
            await message.answer("Вы уже зарегистрированы.", 
                                 reply_markup=admin_menu())
        else:
            await message.answer("Вы уже зарегистрированы.", 
                                 reply_markup=gift_sent_button())
        return
    
    rules = (
        "Привет, это бот для тайного Санты!\n\n"
        "Правила:\n"
        "1) Подарок должен быть не дороже 500 рублей\n"
        "2) Только анонимное дарение (например, втихую положите подарок на стол)\n\n"
        "Регистрация:\n"
        "Введите ваше имя:"
    )
    await message.answer(rules)
    await state.set_state(Form.waiting_for_name)

@router.message(Form.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично! А теперь расскажи о своих увлечениях:")
    await state.set_state(Form.waiting_for_hobbies)

@router.message(Form.waiting_for_hobbies)
async def process_hobbies(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    hobbies = message.text

    db = get_db()
    user = db.query(Users).filter(Users.telegram_id 
                                  == message.from_user.id).first()
    user.name = name
    user.hobbies = hobbies
    db.commit()

    if user.is_admin:
        await message.answer("Вы успешно зарегистрировались!", 
                             reply_markup=admin_menu())
    else:
        await message.answer("Вы успешно зарегистрировались!", 
                             reply_markup=gift_sent_button())
    await state.clear()

@router.message(F.text == "Подарил подарок")
async def gift_send(message: Message):
    db = get_db()
    user = db.query(Users).filter(Users.telegram_id == message.from_user.id).first()

    if not user:
        await message.answer("Сначала заполните анкету.")
        return

    if not user.name:
        await message.answer("Сначала заполните анкету.")
        return

    if user.recipient_id is None:
        await message.answer("Еще не назначен получатель. \
                             Что ты там кому подарил?.")
        return

    user.gift_sent = True
    db.commit()
    await message.answer("Супер! Подарок отмечен как отправленный.")