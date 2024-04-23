from aiogram import types

lang_kb = [
  [
    types.InlineKeyboardButton(text="Русский", callback_data="btn_ru"),
    types.InlineKeyboardButton(text="English", callback_data="btn_en")
  ]
]
language_menu = types.InlineKeyboardMarkup(inline_keyboard=lang_kb)
