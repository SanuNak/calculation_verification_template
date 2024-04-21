import pandas as pd

from typing import Union, List


def save_df_into_xls(
    sheet_names_list: List = ["Лист1"],
    list_dfs: Union[List[pd.DataFrame], pd.DataFrame] = None,
    xls_path: str = None,
) -> None:
    """Функция, сохраняющая DF в форсате XLS"""

    if isinstance(list_dfs, pd.DataFrame):
        list_dfs = [list_dfs]

    if sheet_names_list is None:
        sheet_names_list = ["Лист1"]

    with pd.ExcelWriter(xls_path) as writer:
        for sheet, df in zip(sheet_names_list, list_dfs):
            df.to_excel(excel_writer=writer, sheet_name=sheet, index=False)


if __name__ == "__main__":
    pass
