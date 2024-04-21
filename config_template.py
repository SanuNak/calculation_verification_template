import os
import locale
from datetime import datetime

from src.project_tools.directories_make import create_and_get_dir_in_core_dir

locale.setlocale(locale.LC_ALL, "ru_RU")

USERNAME = "___"
PASSWORD = "__"
ENCODING = "UTF-8"

# коммент для тестирования, чтобы через консоль по сто раз не вводить данные.
# при тест-нии три последующие строки надо раскомитить, закомитить
# YEAR = "2022"
# MONTH = "08"
# CUSTOM_PATH = "C:\\macros\\2. project_promo_svnc\\experiments\\data\\2022\\08"

# *** Справочник дат ***
YEAR = str(input("Введите год отчетного месяца СВНЦ в формате *2022*: ")) or None
MONTH = str(input("Введите отчетный месяц ГИС ТЭК в формате *08*: ")) or None

YEAR_MONTH_DAY = YEAR + MONTH + "01"
MONTH_TEXTMONTH = (
    MONTH + "_" + datetime.strptime(YEAR_MONTH_DAY, "%Y%m%d").strftime("%B")
)

# *** Ссылки на папки с отчетами для загрузки ***
CUSTOM_PATH = (
    input(
        "\nВведите путь до тестовой папки с отчетами системы,\n"
        "иначе выбираем report_out одной из систем СВНЦ: \n"
    )
    or None
)

ORCT_FOLDERS = (
    "//Vm-dfr-files\\департамент_финансовых_расчетов"
    "\\Отдел_расчета_цен_трансляции\\_Общая\\4. ГИСТЕК"
    "\\1 Данные для ГИСТЕК\\"
)

# Создаем каталог для выгружаемых отчетов
REPORT_OUT_PATH = create_and_get_dir_in_core_dir(
    dir_name="report_out", year=YEAR, month=MONTH
)


# Список наименований разделов для распарсенного итоговоого XML без UUID

NAMES_XML_PARTS = [
    "Раздел_1",
    "Раздел_20",
    "Раздел_23",
    "Раздел_300",
    "Раздел_301",
    "Раздел_4",
    "Раздел_5",
    "Раздел_6",
    "Раздел_71",
    "Раздел_72",
]


def get_path_to_original_reports() -> str:
    """Выбираем путь к файлам"""

    if CUSTOM_PATH is not None:
        return CUSTOM_PATH
    else:
        return os.path.join(ORCT_FOLDERS, YEAR, MONTH_TEXTMONTH)


def chosing_rio_bd() -> str:
    """Функция для получения БД выбранного при запуске"""

    # *** Справочник стендов РИО ***
    RIO_URL = {
        "1": "vm-riogreen-db.rosenergo.com:1521/riogreen.rosenergo.com",
        "2": "vm-frs9i2a-db.rosenergo.com:1521/frs9i2.rosenergo.com",
        "3": "vm-riogtan-db.rosenergo.com:1521/riotan.rosenergo.com",
        "4": "vm-riolime-db.rosenergo.com:1521/riolime.rosenergo.com",
    }

    print("\n*** Выбираем БД РИО ***")
    print("  *** Если бд рио грин, то введите:", "1")
    print("  *** Если бд рио боевой, то введите:", "2")
    print("  *** Если бд рио тан, то введите:", "3")
    print("  *** Если бд рио лайм, то введите:", "4 \n")

    CHOSING_RIO_BD = RIO_URL[
        str(
            input("Введите номер БД РИО, по умолчанию смотрим на промышленный>: \n")
            or "2"
        )
    ]
    return CHOSING_RIO_BD


def chosing_gistek_bd() -> str:
    """Функция для получения БД выбранного при запуске"""

    # *** Справочник стендов РИО ***
    GISTEK_URL = {
        "1": "lp-a7o11-90.rosenergo.com:1521/gistkcyn.rosenergo.com",
        "2": "lp-a6o11-182.rosenergo.com:1521/gistkred.rosenergo.com",
        "3": "lp-a6o11-212.rosenergo.com:1521/gistktan.rosenergo.com",
    }

    print("\n*** Выбираем БД ГИСТЭК ***")
    print("  *** Если бд гистэк циан, то введите:", "1")
    print("  *** Если бд гистэк боевой, то введите:", "2")
    print("  *** Если бд гистэк тан, то введите:", "3")

    CHOSING_GISTEK_BD = GISTEK_URL[
        str(
            input("Введите номер БД ГИСТЭК, по умолчанию смотрим на промышленный>: \n")
            or "2"
        )
    ]
    return CHOSING_GISTEK_BD


if __name__ == "__main__":
    pass
