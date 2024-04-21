import config
import pandas as pd
import os

from src.project_tools.excel_parsing import excel_parsing

# определяем путь к файлам.
if config.CUSTOM_PATH:  # если указан путь к тестовой папке то берем его
    path_to_reports = os.path.join(config.get_path_to_original_reports())
else:  # если НЕ указан путь к тестовой папке, то берем станд-й путь + подпапка
    path_to_reports = os.path.join(
        config.get_path_to_original_reports(), "ФРС БР НЦЗ"
    )


def _split_potr_gener_br_ncz(row):
    """Разделение объема призводства и потребления для P5 _нцз.
    Сейчас факт для ГТП потребления и генерации в отдном столбце
    """
    type = row[0]
    # т.е. если тип ГТП начинается с г (генерация),то определяем BR_VG_GTP_FACT
    if type[:1] == "г":
        row[3] = row[2]
        row[4] = 0
    # т.е. если тип ГТП начинается с п (потребление),то определяем BR_VC_GTP_FACT
    elif type[:1] == "п":
        row[3] = 0
        row[4] = row[2]
    return row


def _get_upz_br_stoim_otkl_s(path: str = path_to_reports) -> pd.DataFrame:
    FILE_MASK = "*UPZ-BR-stoim_otkl-S*"
    SKIPROWS = 6
    SKIPFOOTER = 0
    USECOLS = [3, 4, 9]
    HEADER = 0
    COLUMNS = ["Тип_ГТП", "Код_ГТП", "Факт"]

    df = excel_parsing(
        path=path_to_reports,
        file_mask=FILE_MASK,
        skiprows=SKIPROWS,
        skipfooter=SKIPFOOTER,
        usecols=USECOLS,
        header=HEADER,
        columns=COLUMNS,
    )
    # Удаляем пустые строки
    df = df.dropna()
    # Создаем новые столбцы, сохраним туда факт потр и генер отдельно
    df["BR_VG_GTP_FACT"] = 0
    df["BR_VC_GTP_FACT"] = 0
    # разделяем общий столбец с Фактом на два толбца, отдельно для генер. и потребл
    data_sib = df.apply(_split_potr_gener_br_ncz, axis=1, result_type="expand")
    # удаляем лишние столбцы (тип ГТП и теперь ненужный общий "Факт")
    data_sib = data_sib.drop(data_sib.columns[[0, 2]], axis="columns")
    # группируем данные по "Код_ГТП", т.е. суммируем все почасовки
    data_sib = data_sib.groupby(["Код_ГТП"]).sum().reset_index()

    data_sib = data_sib[data_sib.iloc[:, 0].str.contains("^F") == False]
    data_sib = data_sib.fillna(0)  # заменяем Nan на 0

    return data_sib


def _get_upz_br_stoim_otkl_e(path: str = path_to_reports) -> pd.DataFrame:
    FILE_MASK = "*UPZ-BR-stoim_otkl-E*"
    SKIPROWS = 6
    SKIPFOOTER = 0
    USECOLS = [3, 4, 11]
    HEADER = 0
    COLUMNS = ["Тип_ГТП", "Код_ГТП", "Факт"]

    df = excel_parsing(
        path=path,
        file_mask=FILE_MASK,
        skiprows=SKIPROWS,
        skipfooter=SKIPFOOTER,
        usecols=USECOLS,
        header=HEADER,
        columns=COLUMNS,
    )
    # Удаляем пустые строки
    df = df.dropna()
    # Создаем новые столбцы, сохраним туда факт потр и генер отдельно
    df["BR_VG_GTP_FACT"] = 0
    df["BR_VC_GTP_FACT"] = 0
    # разделяем общий столбец с Фактом на два толбца, отдельно для генер. и потребл
    data_sib = df.apply(_split_potr_gener_br_ncz, axis=1, result_type="expand")
    # удаляем лишние столбцы (тип ГТП и теперь ненужный общий "Факт")
    data_sib = data_sib.drop(data_sib.columns[[0, 2]], axis="columns")
    # группируем данные по "Код_ГТП", т.е. суммируем все почасовки
    data_sib = data_sib.groupby(["Код_ГТП"]).sum().reset_index()

    data_sib = data_sib[data_sib.iloc[:, 0].str.contains("^F") == False]
    data_sib = data_sib.fillna(0)  # заменяем Nan на 0

    return data_sib


def get_upz_br_stoim_otkl_united() -> pd.DataFrame:
    """
    Объединяем результат из отчетов по Европе и отчета по Сибири
    """
    df_sib = _get_upz_br_stoim_otkl_s()
    df_eur = _get_upz_br_stoim_otkl_e()
    df_united = pd.concat([df_sib, df_eur], ignore_index=True, sort=False)
    return df_united


if __name__ == "__main__":
    print(get_upz_br_stoim_otkl_united())
