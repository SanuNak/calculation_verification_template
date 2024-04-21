import pandas as pd

from config import chosing_gistek_bd, YEAR_MONTH_DAY
from src.project_tools.coonection_db import conn_db
from src.project_tools.sql_query_list import get_sql_query_br_from_db_gistek


def get_br_from_db() -> pd.DataFrame:
    """Получение данных загруженных из БР в БД ГИСТЭК"""
    sql_query_br_data = get_sql_query_br_from_db_gistek(YEAR_MONTH_DAY)
    gisteks_db_name = chosing_gistek_bd()

    df_br_data = conn_db(chosing_bd=gisteks_db_name, sql_query=sql_query_br_data)
    return df_br_data


if __name__ == "__main__":
    print(get_br_from_db())
