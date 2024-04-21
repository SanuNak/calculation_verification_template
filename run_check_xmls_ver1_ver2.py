import time

from src.check_reports.public_reports.xml_to_minenergo_cheks import (
    check_ats_xml_ver1_with_db,
    check_ats_xml_ver1_with_external_files,
)



def main() -> None:
    """Проверка XML без UUID и XML c UUID, который передается в Минэнерго"""

    # проверка XML версии 1 без UUID
    check_ats_xml_ver1_with_db() # с данными из БД системы  ГИСТЭК
    check_ats_xml_ver1_with_external_files() # с данными из отчетов коллег

    # проверка XML версии 2 с UUID, который загружаем на портале ГИСТЭК
    # проверяем правильность формирования XML на основе XML версии 1  без UUID
    # check_ats_xml_ver2_()


if __name__ == "__main__":
    print("*** Старт скрипта\n")
    start_time = time.time()

    main()

    print("\nВремя проверки: {:.2f} мин".format(time.time() / 60 - start_time / 60))
