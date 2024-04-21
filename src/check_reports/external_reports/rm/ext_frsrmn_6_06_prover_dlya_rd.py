import config
import pandas as pd
import os

from src.project_tools.excel_parsing import excel_parsing


def get_check_node_prices() -> pd.DataFrame:
    FILE_MASK = "*_check_node_prices*"
    SKIPROWS = 4
    SKIPFOOTER = 0
    USECOLS = [1, 2, 3, 4, 5]
    HEADER = 0
    COLUMNS = ["Название_участника", "Код_ГТП", "Код_узла", "kcq,n", "λузлn,h"]

    path_to_system_reports = os.path.join(
        config.get_path_to_original_reports(), "Мини_хд"
    )

    df_node_prices = excel_parsing(
        path=path_to_system_reports,
        file_mask=FILE_MASK,
        skiprows=SKIPROWS,
        skipfooter=SKIPFOOTER,
        usecols=USECOLS,
        header=HEADER,
        columns=COLUMNS,
    )

    # Замещаем Nan значением сверху
    df_node_prices["Название_участника"].fillna(method="ffill", inplace=True)
    # Замещаем Nan значением сверху
    df_node_prices["Код_ГТП"].fillna(method="ffill", inplace=True)
    # Убираем пустые строки без цен и коэффициентов
    df_node_prices = df_node_prices.loc[
        (df_node_prices["kcq,n"].isna() != True)
        | (df_node_prices["λузлn,h"].isna() != True)
    ]

    return df_node_prices


if __name__ == "__main__":
    pass
