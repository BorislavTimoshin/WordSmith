class Message:
    """ Класс работает с сообщениями:
     1) способен удалять сообщения
     2) выводить сообщения """
    def __init__(self, bot_obj):
        self.bot_obj = bot_obj

    async def delete_last_message(self, human_id, message_id):
        """ Метод, удаляющий предыдущее сообщение """
        await self.bot_obj.delete_message(human_id, message_id)

    async def output_text(self, human_id, text, menu=None):
        """ Метод, печатающий текст с меню/без меню """
        if menu is None:  # Если меню нет
            await self.bot_obj.send_message(human_id, text, parse_mode="HTML")  # Выводим текст
        else:  # Иначе выводим текст с меню
            await self.bot_obj.send_message(human_id, text, reply_markup=menu, parse_mode="HTML")

    async def delete_and_output_text(self, human_id, message_id, text, menu=None):
        """ Метод, удаляющий предыдущее сообщение и печатающий текст с меню/без меню """
        await self.delete_last_message(human_id, message_id)
        await self.output_text(human_id, text, menu)
