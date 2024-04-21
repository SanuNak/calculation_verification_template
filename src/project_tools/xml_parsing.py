import glob
import os
import xml.etree.cElementTree as ET

import pandas as pd
from typing import List, Union


def _get_list_files(
        path_to_project: str,
        file_mask: str) -> Union[List, List[Union[bytes, str]]]:
    """Получение списка xml"""
    path_f = glob.glob(os.path.join(path_to_project, file_mask), recursive=False)
    return path_f


def parsing_standart_xml(
    path_to_project: str,
    file_mask: str,
    cols_name: List[str],
    parameters: List[str],
    root_iter: str,) -> pd.DataFrame:
    """Функция для распарсивания стандартного XML"""

    # Получаем список XML для обработки
    xml_files = _get_list_files(path_to_project, file_mask)

    # Получаем результат разбора XML (может быть больше одного)
    for xml_file in xml_files:
        tree = ET.ElementTree(file=xml_file)
        root = tree.getroot()
        row = {}
        data = []

        # Parsing of xmlfile
        for child in root.iter(root_iter):
            # First, we correlate the parameters and column names
            # Then we create a dictionary with the name of the parameter and its value
            row.update(
                {
                    col_name: child.attrib.get(parameter)
                    for col_name, parameter in zip(cols_name, parameters)
                }
            )

            data.append(row)
            row = {}

        df_from_xml = pd.DataFrame(data)  # Запись в DataFrame

    return df_from_xml


def parsing_xml_ats_minenergo(
        path_to_project: str,
        file_mask: str) -> List[dict]:
    """Функция для распарсивания XML ATS_MINENERGO_F456.xml"""

    # Получаем список XML для обработки
    xml_files = _get_list_files(path_to_project, file_mask)

    # функция для распарсивания XML на список словарей
    tree = ET.ElementTree(file=xml_files[0])
    root = tree.getroot()
    d = {}
    data = []
    data_1 = []
    data_20 = []
    data_23 = []
    data_300 = []
    data_301 = []
    data_4 = []
    data_5 = []
    data_6 = []
    data_71 = []
    data_72 = []

    # Перебираем все теги strfree в XML
    for all_level in root.iter("strfree"):
        StrfreeCode = all_level.attrib.get("code")  # код раздела

        if int(StrfreeCode[0:1:1]) == 1:
            # Перебор подтегов <column> Раздела 1, и так далее для каждого раздела
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_1.append(d)
                d = {}

        elif int(StrfreeCode[0:2:1]) == 20:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_20.append(d)
                d = {}

        elif int(StrfreeCode[0:2:1]) == 23:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_23.append(d)
                d = {}

        elif int(StrfreeCode[0:3:1]) == 300:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_300.append(d)
                d = {}

        elif int(StrfreeCode[0:3:1]) == 301:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_301.append(d)
                d = {}

        elif int(StrfreeCode[0:1:1]) == 4:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_4.append(d)
                d = {}

        elif int(StrfreeCode[0:1:1]) == 5:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_5.append(d)
                d = {}

        elif int(StrfreeCode[0:1:1]) == 6:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_6.append(d)
                d = {}

        elif int(StrfreeCode) == 70001:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_71.append(d)
                d = {}

        elif int(StrfreeCode) == 70002:
            # Перебор подтегов <column>
            for col in all_level.findall(".//column"):
                name = col.attrib.get("name")
                value = col.text
                # сохраням параметры из XML
                d.update({"StrfreeCode": StrfreeCode})
                d.update({"name": name})
                d.update({"value": value})
                data_72.append(d)
                d = {}

    data.append(data_1)
    data.append(data_20)
    data.append(data_23)
    data.append(data_300)
    data.append(data_301)
    data.append(data_4)
    data.append(data_5)
    data.append(data_6)
    data.append(data_71)
    data.append(data_72)

    return data


if __name__ == "__main__":
    pass
