import cx_Oracle
import pandas as pd
from typing import Union

from config import USERNAME
from config import PASSWORD
from config import ENCODING



def conn_db(chosing_bd: str, sql_query: str) -> Union[pd.DataFrame, None]:
    """Функция для подключения к БД
    chosing_bd: - указывается выбранная БД
    sql_query: - указывается текст запроса к БД
    """

    try:
        connection = cx_Oracle.connect(
            USERNAME, PASSWORD, chosing_bd, encoding=ENCODING
        )

        cursor = connection.cursor()

        # Выполняем запрос с обработкой исключений
        try:
            cursor.execute(sql_query)
            mydata = [x for x in cursor.fetchall()]
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame(data=mydata, columns=columns)
        except cx_Oracle.DatabaseError as e:
            df = None
            print(f"!!! Проблемы с запросом. Вот ошибка - {e}\n")

        cursor.close()

    except cx_Oracle.Error as error:
        print(f"!!! Проблемы с подключением. Вот ошибка - {error}")
    except:
        print("!!! Неопознаная ошибка")
    finally:
        # Закрываем соединение
        if connection:
            connection.close()

    return df


if __name__ == "__main__":
    pass
