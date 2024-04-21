import glob
import os
import pandas as pd

from typing import Any, List, Union


def _get_files_path_list(
    path_to_system_reports: str, file_mask: str
) -> Union[List[Union[bytes, str]], str, None]:
    """Получаем список файлов с путями"""
    path_preparation = os.path.join(path_to_system_reports, file_mask)
    file_list = glob.glob(path_preparation, recursive=True)

    # Проверяем, существуют ли файлы по заданному пути
    try:
        os.path.exists(file_list[0])
        print("***", f"Файлы с маской {file_mask} загружены")
        return file_list
    except:
        print("!" * 5, f"Файлы с маской {file_mask} НЕ найдены")
        return "no files"


def excel_parsing(
    path: str,
    file_mask: str,
    usecols: List[int],
    skiprows: int,
    skipfooter: int,
    header: int,
    columns: List[str],
) -> Union[Any, None]:
    """
    Функция для распарсивания нескольких XLS
    По параметрам можно уточнить в доках по функции pandas pd.read_excel
    """

    # получаем список файлов с путями
    files_list = _get_files_path_list(path, file_mask)

    df_part = []

    # Обработка в случае отсустсвия файлов с заданной маской
    if files_list == "no files":
        return None

    # Перебираем файлы и сохраняем данные в один масив
    for file in files_list:
        with pd.ExcelFile(file) as xls:
            data = pd.read_excel(
                xls,
                skiprows=skiprows,
                skipfooter=skipfooter,
                usecols=usecols,
                header=header,
                sheet_name=None,
            )
            if isinstance(data, dict):
                # соединялка в случае нескольких листов в файле ексель
                # сперва преобразуем словарь в список значений словаря
                data_list =  [v for k, v in data.items()]
                # потом объединяем элементы списка, т.е. все листы ексель в один DF
                df = pd.concat(data_list, ignore_index=True, sort=False)
                # добавляеям полученный DF в общий список для всех возможных файлов
                df_part.append(df)
            elif isinstance(df, pd.DataFrame):
                # добавляем DF из одного файла в общий список для всех возможных файлов
                df_part.append(df)
            else:
                print("!!! Ошибка разбора ексель !!!")
    # объединяем результат из всех ексель в один датафрейм
    df_concat = pd.concat(df_part, ignore_index=True, sort=False)
    df_concat.columns = columns  # меняем наименования параметрова в шапке
    return df_concat


if __name__ == "__main__":
    pass
