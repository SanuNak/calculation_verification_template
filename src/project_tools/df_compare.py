import pandas as pd


def df_compare(first_df: pd.DataFrame, second_df: pd.DataFrame) -> pd.DataFrame:
    """СравненИе двух DataFrame. Метода сравнения: два DataFrame объединяются,
    потом удаляются дупликаты и остаются только отсортированные разночтения"""
    diff_col = (
        pd.concat([first_df, second_df], ignore_index=True)
        .drop_duplicates(keep=False)
        .sort_values(["Код_ГТП", "Код_узла"])
    )
    return diff_col


if __name__ == "__main__":
    pass
