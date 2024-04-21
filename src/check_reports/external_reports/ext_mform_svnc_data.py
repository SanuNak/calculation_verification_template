import numpy as np
import os
import pandas as pd
import config

from src.project_tools.xml_parsing import parsing_standart_xml

# определяем путь к файлам.
if config.CUSTOM_PATH:  # если указан путь к тестовой папке то берем его
    path_to_system_reports = os.path.join(config.get_path_to_original_reports())
else:  # если НЕ указан путь к тестовой папке, то берем стандрт-й путь + подпапка
    path_to_system_reports = os.path.join(
        config.get_path_to_original_reports(), "МФО РМ"
    )


def get_mform_svnc_data_pok(path: str = path_to_system_reports) -> pd.DataFrame:
    """Парсинг файла mform_svnc_data Покупка и его конвертация в DataFrame"""
    FILE_MASK = "*MFORM_SVNC_DATA_*"
    PARAMETERS = [
        "participant-code",
        "DPG-code",
        "N_gtp_sdm_pok_sdm",
        "N_gtp_sdm_pok_sdem",
    ]
    COLS_NAME = [
        "participant_code",
        "DPG_code",
        "N_gtp_sdm_pok_sdm",
        "N_gtp_sdm_pok_sdem",
    ]
    ROOT_ITER = "DPG-month"

    df = parsing_standart_xml(
        path_to_project=path,
        file_mask=FILE_MASK,
        cols_name=COLS_NAME,
        parameters=PARAMETERS,
        root_iter=ROOT_ITER,
    )

    # переводим числовые данные в соответствующий тип
    df[["N_gtp_sdm_pok", "N_gtp_sdm_pok_sdm", "N_gtp_sdm_pok_sdem"]] = df[
        ["N_gtp_sdm_pok", "N_gtp_sdm_pok_sdm", "N_gtp_sdm_pok_sdem"]
    ].astype(np.float64)
    return df


def get_mform_svnc_data_prod(path: str = path_to_system_reports) -> pd.DataFrame:
    """Парсинг файла mform_svnc_data Продажа и его конвертация в DataFrame"""
    FILE_MASK = "*MFORM_SVNC_DATA_*"
    PARAMETERS = [
        "participant-code",
        "DPGG-code",
        "N_gtp_sdm_pok_sdm",
        "N_gtp_sdm_pok_sdem",
    ]
    COLS_NAME = [
        "participant_code",
        "DPGG_code",
        "N_gtp_sdm_pok_sdm",
        "N_gtp_sdm_pok_sdem",
    ]
    ROOT_ITER = "DPG-month"

    df = parsing_standart_xml(
        path_to_project=path,
        file_mask=FILE_MASK,
        cols_name=COLS_NAME,
        parameters=PARAMETERS,
        root_iter=ROOT_ITER,
    )

    # переводим числовые данные в соответствующий тип
    df["N_gtp_sdm_prod_sdm", "N_gtp_sdm_prod_sdem"] = df[
        ["N_gtp_sdm_prod_sdm", "N_gtp_sdm_prod_sdem"]
    ].astype(np.float64)
    return df


if __name__ == "__main__":
    pass
