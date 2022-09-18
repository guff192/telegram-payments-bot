from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.services.course import list_courses


_courses_list = list_courses()
courses_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
courses_keyboard.add(*(KeyboardButton(course.name) for course in _courses_list))

