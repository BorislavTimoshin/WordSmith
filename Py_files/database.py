import sqlite3


# Класс для работы с базой данных
class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def set_person(self, human_id: int) -> None:
        with self.connection:
            self.cursor.execute(
                "INSERT INTO `Users` (`human_id`) VALUES (?)",
                (human_id,)
            )
            self.connection.commit()

    def person_exists(self, human_id: int) -> bool:
        with self.connection:
            result = self.cursor.execute(
                "SELECT `human_id` FROM `Users` WHERE `human_id` = ?",
                (human_id,)
            ).fetchall()
            return bool(result)

    def delete_person(self, human_id: int) -> None:
        with self.connection:
            self.cursor.execute(
                "DELETE FROM `Users` WHERE `human_id` = ?",
                (human_id,)
            )

    def set_language(self, human_id: int, language: str) -> None:
        self.cursor.execute(
            "UPDATE `Users` SET `language` = ? WHERE `human_id` = ?",
            (language, human_id,)
        )
        self.connection.commit()

    def get_language(self, human_id: int) -> str:
        with self.connection:
            result = self.cursor.execute(
                "SELECT `language` FROM `Users` WHERE `human_id` = ?",
                (human_id,)
            ).fetchall()
            for i in result:
                return i[0]


# Экземпляр класса для работы с бд
db = Database('data/database')
