from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from bot.database.session import get_db
from bot.database.models import Users
from bot.utils.lottery import loterry
from bot.config import ADMIN_IDS
from bot.keyboards.keyboards import admin_menu

router = Router()

@router.message(Command("start_lottery"))
async def start_lottery(message: Message, bot: Bot):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    db = get_db()
    users = db.query(Users).filter(Users.name.isnot(None)).all()

    if not users:
        await message.answer("Пока никто не проявил желание участвовать (или все слились).")
        return

    if len(users) < 2:
        await message.answer("Хотя бы 2 должны изъявить желание, если все решили слиться.")
        return

    pairs = loterry(users)

    for giver, recipient in pairs:
        giver_user = db.query(Users).filter(Users.telegram_id == giver.telegram_id).first()
        giver_user.recipient_id = recipient.id
        db.commit()

        msg = f"Вы дарите подарок: {recipient.name}, а его увлечения: {recipient.hobbies}"
        await bot.send_message(giver.telegram_id, msg)

    await message.answer("Жеребьёвка завершена. Участники получили информацию.", 
                         reply_markup=admin_menu())


@router.message(lambda m: m.text == "Начать жеребьевку")
async def lottery_button(message: Message, bot: Bot):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    await start_lottery(message, bot)