import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import keyboards as kb

import config

router = Router()

class FormStates(StatesGroup):
    name = State()
    age = State()
    gender = State()
    telephone_number = State()


@router.message(CommandStart())
async def start_message(message: Message, state: FSMContext):
    if message.from_user.id == config.ADMIN_ID:
        await message.answer('Добро пожаловать администратор', reply_markup=kb.admin_main)
    else:
        await state.set_state(FormStates.name)
        await message.answer('Здравствуйте! Ваше имя?')

@router.message(FormStates.name, F.text)
async def name_form(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormStates.age)
    await message.answer(f'Приятно было познакомится {message.text}, Мне нужно знать ваш возраст')

@router.message(FormStates.age, F.text)
async def age_form(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(FormStates.gender)
    await message.answer(f'Ваш пол?', reply_markup=kb.gender_main)

@router.callback_query(FormStates.gender, F.data)
async def gender_form(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'male':
        await state.update_data(gender='мужской')
    if callback.data == 'female':
        await state.update_data(gender='женский')

    await callback.message.answer('Данные добавлены. Задания и лекции будут отправлятся вам каждый день по расписанию,'
                          ' а ваши достижения будут сохранятся. Первое задание вы получите сейчас', reply_markup=kb.move_main)
    await callback.message.answer("*Задание*")

@router.message(F.text)
async def unfamiliar_text(message: Message):
    await message.reply('Я вас не понимаю')