import os
import pandas as pd

import config
from src.project_tools.excel_parsing import excel_parsing


def get_uch_reference() -> pd.DataFrame:
    """Загрузка Кодов ГТП из справочника полученного от коллег из РЭА"""

    # Определение параметров для функции распарсивания XLS excel_parsing()
    FILE_MASK = "*Справочник Участников_код.xls*"
    SKIPROWS = 0
    SKIPFOOTER = 0
    USECOLS = None
    HEADER = 0
    COLUMNS = ["id_Участника", "Код_участника", "Наименование_участника"]

    # определяем путь к файлам.
    if config.CUSTOM_PATH:  # если указан путь к тестовой папке то берем его
        path_to_reports = os.path.join(config.get_path_to_original_reports())
    else:  # если НЕ указан путь к тестовой папке, то берем станд-й путь + подпапка
        path_to_reports = os.path.join(
            config.get_path_to_original_reports(), "СубСостав", "от РЭА"
        )

    df_uch_reference = excel_parsing(
        path=path_to_reports,
        file_mask=FILE_MASK,
        skiprows=SKIPROWS,
        skipfooter=SKIPFOOTER,
        usecols=USECOLS,
        header=HEADER,
        columns=COLUMNS,
    )
    return df_uch_reference


if __name__ == "__main__":
    pass
