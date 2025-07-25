from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

class DB_Session():
    '''
    Класс для работы с БД
    '''
    def __init__(self) -> None:
        self.username = 'root' 
        self.password = 'mysql123'
        self. host = 'localhost'
        self.database_name = 'users'

    # Соединение с бд
        self.DATABASE_URL = f"mysql+pymysql://{self.username}:{self.password}@{self.host}/{self.database_name}"

    # Соединение движка sqlalchemy
        self.engine = create_engine(self.DATABASE_URL, echo=True)
        self.Session = sessionmaker(bind=self.engine)

        # Создание сессии
        self.session = self.Session()

    def table_lookup(self, table: str):
        '''
        функция показывает данные, хранящиеся в одной из таблиц по запросу
        '''
        self.session = self.Session()
        try:
            query = text("SELECT * FROM users")

            # Execute the query and fetch results
            result = self.session.execute(query).fetchall()
            return result
        except Exception as e:
            self.session.close()
            return f"Error: {e}"

    def add_user(self, login: str, password: str):
        '''
        функция добавляет пользователя в таблицу users (логин и пароль)
        '''
        try:
            self.session.execute(
                text("INSERT INTO users (login, password) VALUES (:login, :password)"),
                {"login": login,"password": password}
            )
            self.session.commit()
            return f"Пользователь '{login}' добавлен успешно!"
        except Exception as e:

            self.session.rollback()
            self.session.close()
            return f"Error: {e}"
    
    def delete_user(self, login: str):
        '''
        Функция удаляет пользователя из таблицы users по логину
        '''
        try:
            result = self.session.execute(
                text("DELETE FROM users WHERE login = :login"),
                {"login": login}
            )
            self.session.commit()

            if result.rowcount > 0:
                return f"Пользователь '{login}' удален успешно!"
            else:
                return f"Пользователь '{login}' не найден."
        except Exception as e:
            self.session.rollback()
            self.session.close()
            return f"Error: {e}"


if __name__ == "__main__":
    session = DB_Session()
    print(session.table_lookup("users"))