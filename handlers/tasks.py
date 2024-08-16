from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from aiogram.utils.i18n import gettext as _
from datetime import datetime, date

import keyboards as kb
from db import Client

router = Router()
client = Client()

class TaskStates(StatesGroup):
    _id = State()
    user_id = State()
    dedline = State()
    description = State()
    status = State()

class DelTaskStates(StatesGroup):
    delete_task = State()


@router.message(F.text == 'Задачи по расписанию')
async def tasks(message: Message):
    await message.reply('Выберите действие', reply_markup=kb.task_main)

@router.message(F.text == 'Задачи по расписанию')
async def tasks(message: Message, state: FSMContext):
    await message.reply('Напишите дедлайн для задания в формате DD.MM.YYYY', reply_markup=kb.cancel_main)

    await state.set_state(TaskStates._id)
    await state.update_data(_id=str(client.tasks_sum()) + '_' + str(message.from_user.id))

    await state.set_state(TaskStates.user_id)
    await state.update_data(user_id=message.from_user.id)

    await state.set_state(TaskStates.dedline)

def parse_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError(_("Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ."))


@router.message(TaskStates.dedline, F.text)
async def ask_date(message: Message, state: FSMContext):
    try:
        user_date = parse_date(message.text)
        await message.answer(f"Вы ввели дату: {user_date.strftime('%d.%m.%Y')}. Напишите описание для задачи",
                             reply_markup=kb.cancel_main)
        await state.update_data(dedline=message.text)
        await state.set_state(TaskStates.description)
    except ValueError as e:
        await message.answer(str(e))

@router.message(TaskStates.description, F.text)
async def task_description(message: Message, state: FSMContext):
    await message.answer('Задача добавлена. За 2 дня до дедлайна будет приходить напоминание',
                         reply_markup=kb.task_main)
    await state.update_data(description=message.text)
    await state.set_state(TaskStates.status)
    await state.update_data(status='Не выполнено')

    data = await state.get_data()
    client.insert_task(data)

    await state.clear()

@router.message(F.text == 'Расписание')
async def tasks_plan(message: Message):
    await message.reply(f'Расписание задач: {client.print_task()}', reply_markup=kb.cancel_main)

@router.message(F.text == 'Изменить статус задачи')
async def task_status(message: Message, state: FSMContext):
    task_list = []
    task_query = ()
    for value in client.task_collection.find(task_query, {"_id": 0, "description": 1}):
        task_list.append(value.get("description"))

    async def change_task_main():
        keyboard = ReplyKeyboardBuilder()
        for task in task_list:
            keyboard.add(KeyboardButton(text=task))
        return keyboard.adjust(2).as_markup()

    await message.reply(f'Выберите задачу статус которого вы хотите изменить',
                        reply_markup=await change_task_main())

    await state.set_state(DelTaskStates.delete_task)

@router.message(DelTaskStates.delete_task, F.text)
async def task_status_choice(message: Message, state: FSMContext):
    await message.reply('Выберите новый статус задачи', reply_markup=kb.task_status_inline)
    await state.update_data(delete_task=message.text)

@router.callback_query(F.data)
async def task_callbacks(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    choiced_task = (state.get_data())

    if callback.data == 'not_comleted':
        await client.update_task_status({f'description": "{choiced_task}"'},
                                        {"$set": {"status": "Не выполнено"}})
    elif callback.data == 'in_progress':
        await client.update_task_status({f'description": "{choiced_task}"'},
                                        {"$set": {"status": "Выполняется"}})
    else:
        await client.update_task_status({f'description": "{choiced_task}"'},
                                        {"$set": {"status": "Выполнено"}})

