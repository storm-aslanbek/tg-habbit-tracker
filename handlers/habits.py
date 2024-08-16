from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram.utils.i18n import gettext as _
from datetime import time

import keyboards as kb
from db import Client

router = Router()
client = Client()

class HabitStates(StatesGroup):
    _id = State()
    user_id = State()
    time = State()
    description = State()

class DelHabit(StatesGroup):
    del_habit_state = State()


@router.message(F.text == 'Ежедневная привычка')
async def dayly_habit(message: Message):
    await message.reply('Выберите что вы хотите сделать', reply_markup=kb.habit_main)


@router.message(F.text == 'Добавить привычку')
async def add_habit(message: Message, state: FSMContext):
    await message.reply('Напишите время для напоминания о привычке в формате HH:MM.',
                        reply_markup=kb.cancel_main)

    await state.set_state(HabitStates._id)
    await state.update_data(_id=str(message.from_user.id) + "_" + str(client.habits_sum()))

    await state.set_state(HabitStates.user_id)
    await state.set_state(HabitStates.user_id)
    await state.update_data(user_id=message.from_user.id)

    await state.set_state(HabitStates.time)

def parse_time(time_str: str) -> time:
    try:
        hours, minutes = map(int, time_str.split(":"))
        return time(hour=hours, minute=minutes)
    except ValueError:
        raise ValueError(_('Неверный формат времени. Пожалуйста, введите время в формате HH:MM.'))


@router.message(HabitStates.time, F.text)
async def ask_time(message: Message, state: FSMContext):
    try:
        user_time = parse_time(message.text)
        await state.update_data(time=message.text)
        await message.answer(f'Вы ввели время: {user_time.strftime("%H:%M")}. Напишите описание для привычки',
                             reply_markup=kb.cancel_main)
        await state.set_state(HabitStates.description)
    except ValueError as e:
        await message.answer(str(e))

@router.message(HabitStates.description, F.text)
async def habit_note(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    habit_data = await state.get_data()
    await message.answer(f'Привычка добавлена. Напоминание по привычке будет приходить'
                         f' каждый день в {habit_data["time"]}',reply_markup=kb.cancel_main)

    client.insert_habit(habit_data)
    await state.clear()

@router.message(F.text == 'Таблица привычек')
async def habits_table(message: Message):
    await message.answer(f'Ваши привычки: \n{client.print_habits()}', reply_markup=kb.cancel_main)

@router.message(F.text == 'Удалить привычку')
async def delete_habit(message: Message, state: FSMContext):
    habit_list = []
    habit_query = ()
    for value in client.habit_collection.find(habit_query, {"_id": 0, "description": 1}):
        habit_list.append(value.get("description"))

    async def del_habit_main():
        keyboard = ReplyKeyboardBuilder()
        for habit in habit_list:
            keyboard.add(KeyboardButton(text=habit))
        return keyboard.adjust(2).as_markup()

    await message.reply('Выберите привычку которую хотите удалить', reply_markup=await del_habit_main())

    await state.set_state(DelHabit.del_habit_state)


@router.message(DelHabit.del_habit_state, F.text)
async def delete_habit_choice(message: Message, state: FSMContext):
    await state.update_data(del_habit_state=message.text)
    await state.clear()
    await message.answer('Привычка удалена', reply_markup=kb.cancel_main)


    client.habit_collection.delete_one({"description": f"{message.text}"})