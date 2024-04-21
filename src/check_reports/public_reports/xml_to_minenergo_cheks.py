import os
import pandas as pd
import numpy as np
from typing import List

import config
from src.project_tools.xml_parsing import parsing_xml_ats_minenergo
from src.project_tools.df_save import save_df_into_xls
from src.project_tools.df_compare import df_compare
from src.check_reports.external_reports.ext_rea_gtp_reference import (
    get_gtp_reference,
)
from src.check_reports.external_reports.ext_rea_uch_reference import (
    get_uch_reference,
)

# путь для сохранения отчета проверки
xml_ver1_path = os.path.join(config.REPORT_OUT_PATH, "xml_ver1_check.xlsx")


def _convert_dict_to_df(dict_data_list: List[dict]) -> List[pd.DataFrame]:
    """Конвертация списка dict-ов в список df"""

    df_list = []
    for dict_data in dict_data_list:
        df = pd.DataFrame(dict_data).from_dict(dict_data)
        df_list.append(df)
    return df_list


def _sub_transf_df_list(
    df: pd.DataFrame,
    reference: pd.DataFrame = None,
    part_name: str = None,
    unit: str = None,
    unit_id: str = None,
    sort_unit: str = None,
) -> pd.DataFrame:
    """Подзадача для трансформации распарсенных данных в удобный вид, по разделам.
    А также сортировка, форматирование точек и типов и тп.
    Отдельно стоит отметить, что для некоторых рахделов еще добавляем
    Соответствующие АТС-овские коды ГТП и Участников в соответствии с id,
    для читабельности.
    """
    try:
        data = []
        columns_name = []

        # замена запятой на точку и преобразования типа в float64
        # для разделов 1 20 23 3 4 5
        if part_name not in ["Раздел_6", "Раздел_71", "Раздел_72"]:
            df["value"] = df["value"].str.replace(",", ".").astype(np.float64)

        # для всех разделов
        df["StrfreeCode"] = pd.to_numeric(df["StrfreeCode"], errors="ignore")
        # создали список с правильно отсортированным именами столбцов
        columns_name = pd.unique(df["name"]).tolist()
        # вставляем в начало списка имен также и "StrfreeCode"
        columns_name.insert(0, "StrfreeCode")

        # для разделов 6 71 72 преобразуем таблицу
        if part_name in ["Раздел_6", "Раздел_71", "Раздел_72"]:
            _df = df.pivot(
                index="StrfreeCode", columns="name", values="value"
            ).reset_index()
        # для остальных разделов преобразуем таблицу немного по другому
        if part_name not in ["Раздел_6", "Раздел_71", "Раздел_72"]:
            _df = df.pivot_table(
                index="StrfreeCode", columns="name", values="value"
            ).reset_index()

        # Для разделов 1 20 23 3 4 5
        # переименовываем столбцы с ГТП на ГТП_id или Участник на id_Участник
        # потом добавляем столбцы с кодами 'Код_ГТП' или 'Код_Участников'
        if part_name in [
            "Раздел_1",
            "Раздел_20",
            "Раздел_23",
            "Раздел_4",
            "Раздел_5",
        ]:
            # переименовываем
            _df.rename(columns={unit: unit_id}, inplace=True)
            columns_name[1] = unit_id
            # Добавляем параметр 'Код_ГТП' или "Код_Участника' в список
            # для задания последовательности
            columns_name.insert(2, sort_unit)

            # теперь вставляем 'Код_ГТП' в df из справочника от коллег из РЭА
            _df = pd.merge(
                _df,
                reference,
                how="left",
                on=[unit_id],
                left_on=None,
                right_on=None,
                left_index=False,
                right_index=False,
                sort=False,
                suffixes=("_ish", "_bd"),
            )

        # для всех разделов выводим в правильном порядке и переименовываем
        _df = _df[columns_name]

        # в разделе 6 переводим некоторые столбцы в числовой тип
        if part_name == "Раздел_6":
            _df.iloc[:, [0, 1, 4, 6, 7, 8, 9, 10, 11]] = _df.iloc[
                :, [0, 1, 4, 6, 7, 8, 9, 10, 11]
            ].astype(float)

        # во всех разделах кроме 71 и 72 делаем сортировку
        if part_name not in ["Раздел_71", "Раздел_72"]:
            _df.sort_values(by=[sort_unit], inplace=True)

        return _df

    except KeyError:
        print(f'        В XML проблема с "{part_name}"')


def _transforming_df_list(df_list):
    """
    Это промежуточная функция. В ней для каждого раздела вызываем подфункцию,
    а при её передаче перечесляем атрибуты для трансформации данных
    """
    data_gtp = get_gtp_reference().iloc[:, :2]
    data_uch = get_uch_reference().iloc[:, :2]

    part1_data = _sub_transf_df_list(
        df=df_list[0],
        reference=data_gtp,
        part_name="Раздел_1",
        unit="ГТП",
        unit_id="id_ГТП",
        sort_unit="Код_ГТП",
    )

    part20_data = _sub_transf_df_list(
        df=df_list[1],
        reference=data_gtp,
        part_name="Раздел_20",
        unit="ГТП",
        unit_id="id_ГТП",
        sort_unit="Код_ГТП",
    )

    part23_data = _sub_transf_df_list(
        df=df_list[2],
        reference=data_uch,
        part_name="Раздел_23",
        unit="Участники",
        unit_id="id_Участника",
        sort_unit="Код_участника",
    )

    part300_data = _sub_transf_df_list(
        df=df_list[3],
        reference=data_uch,
        part_name="Раздел_300",
        sort_unit="Субъекты РФ",
    )

    part301_data = _sub_transf_df_list(
        df=df_list[4],
        reference=data_uch,
        part_name="Раздел_301",
        sort_unit="Неценовые зоны",
    )

    part4_data = _sub_transf_df_list(
        df=df_list[5],
        reference=data_gtp,
        part_name="Раздел_4",
        unit="ГТП",
        unit_id="id_ГТП",
        sort_unit="Код_ГТП",
    )

    part5_data = _sub_transf_df_list(
        df=df_list[6],
        reference=data_gtp,
        part_name="Раздел_5",
        unit="ГТП",
        unit_id="id_ГТП",
        sort_unit="Код_ГТП",
    )

    part6_data = _sub_transf_df_list(
        df=df_list[7],
        part_name="Раздел_6",
        sort_unit="Код ГТП",
    )

    part71_data = _sub_transf_df_list(
        df=df_list[8], part_name="Раздел_71", sort_unit=None
    )

    part72_data = _sub_transf_df_list(
        df=df_list[9], part_name="Раздел_72", sort_unit=None
    )

    trasformed_df_list = [
        part1_data,
        part20_data,
        part23_data,
        part300_data,
        part301_data,
        part4_data,
        part5_data,
        part6_data,
        part71_data,
        part72_data,
    ]
    return trasformed_df_list


def _db_part1_df():
    pass


def _db_part20_df():
    pass


def _db_part23_df():
    pass


def _db_part300_df():
    pass


def _db_part301_df():
    pass


def _db_part4_df():
    pass


def _db_part5_df():
    pass


def _db_part6_df():
    pass


def _db_part71_df():
    pass


def _db_part72_df():
    pass


def get_prepared_xml_ats_minenergo() -> List[pd.DataFrame]:
    """Парсинг файла xml_ats_minenergo и его конвертация в DataFrame"""
    FILE_MASK = "*ATS_MINENERGO_F456.xml"
    PARAMETERS = ["participant-code", "region-code"]

    # получаем путь к выгруженному XML без UUID
    if config.CUSTOM_PATH:  # если указан путь к тестовой папке то берем его
        path_to_reports = os.path.join(config.get_path_to_original_reports())
    else:  # если НЕ указан путь к тестовой папке, то берем станд-й путь + подпапка
        path_to_reports = os.path.join(
            config.get_path_to_original_reports(), "1_Файлы в Минэнерго"
        )

    # парсим xml и получаем список dict-ов
    df_xml_ats_minenergo = parsing_xml_ats_minenergo(
        path_to_project=path_to_reports, file_mask=FILE_MASK
    )

    # конверитируем список dict-ов в список df
    df_list = _convert_dict_to_df(df_xml_ats_minenergo)

    # доработка полученного списка df для читабельности
    transform_df_list = _transforming_df_list(df_list)

    return transform_df_list


def check_ats_xml_ver1_with_db():
    """
    Эта функция запускает проверки XML для минэнерго с данными из БД системы ГИСТЭК
    """

    # Загрузка данных из XML ver1. Возвращается список DF
    xml_ver1_df_list = get_prepared_xml_ats_minenergo()

    # В качестве примера сохраняем результат в виде екселя с листами для
    # каждого раздела. Можно удалить.
    test_path = os.path.join(config.REPORT_OUT_PATH, "test_file.xlsx")
    save_df_into_xls(config.NAMES_XML_PARTS, xml_ver1_df_list, test_path)

    # Нужно собрать такой же список DF из эталонных отчетов коллег и тп
    db_part1_df = _db_part1_df()
    db_part20_df = _db_part20_df()
    db_part23_df = _db_part23_df()
    db_part300_df = _db_part300_df()
    db_part301_df = _db_part301_df()
    db_part4_df = _db_part4_df()
    db_part5_df = _db_part5_df()
    db_part6_df = _db_part6_df()
    db_part71_df = _db_part71_df()
    db_part72_df = _db_part72_df()

    db_df_list = [
        db_part1_df,
        db_part20_df,
        db_part23_df,
        db_part300_df,
        db_part301_df,
        db_part4_df,
        db_part5_df,
        db_part6_df,
        db_part71_df,
        db_part72_df,
    ]

    # После сборки у нас будут два одинкаовых списка с DF их нужно будет сравнить.
    # Так как df_compare сверяет по одному DF, то в данном случае можем сделать
    # сравнение через цикл

    # цикл с фукцией сравнения и сохранения результата закомментирована.
    # Пока не готов db_df - будет ошибка

    # for name_part, xml_ver1_df, db_df in zip(
    #     config.NAMES_XML_PARTS, xml_ver1_df_list, db_df_list
    # ):

        # result_check = df_compare(xml_ver1_df, db_df)

        # сохраняем результат в виде екселя с листами для каждого раздела
        # save_df_into_xls(
        #     sheet_names_list=name_part,
        #     list_dfs=result_check,
        #     xls_path=xml_ver1_path,
        # )


def check_ats_xml_ver1_with_external_files():
    """Эта функция запускает проверки XML для минэнерго с данными из отчетов коллег"""
    pass


if __name__ == "__main__":
    pass
