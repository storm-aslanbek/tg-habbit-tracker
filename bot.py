import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import keyboards

router = Router()

class FormStates(StatesGroup):
    name = State()
    age = State()
    gender = State()
    telephone_number = State()


@router.message(CommandStart())
async def start_message(message: Message, state: FSMContext):
    await state.set_state(FormStates.name)
    await message.reply('Здравствуйте! Ваше имя?')

@router.message(FormStates.name, F.text)
async def name_form(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormStates.age)
    await message.reply(f'Приятно было познакомится {message.text}, Мне нужно знать ваш возраст')

@router.message(FormStates.age, F.text)
async def age_form(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(FormStates.gender)
    await message.reply(f'Ваш пол?', reply_markup=keyboards.gender_main)

@router.callback_query(FormStates.gender, F.data)
async def gender_form(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'male':
        await state.update_data(gender='мужской')
        await callback.message.answer('Ваш пол мужской')
    if callback.data == 'female':
        await state.update_data(gender='женский')
        await callback.message.answer('Ваш пол женский')

dd