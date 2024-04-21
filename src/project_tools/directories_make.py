import os


def create_and_get_dir_in_core_dir(dir_name, year, month) -> str:
    """
    Функцуия, создающая каталог в корне проекта, также возвращается ссылка на негоёи
    dir_name: - на вход требуется имя каталога, например "report_out"
    year: - указываем год, ножно брать константу из config
    month: - указываем месяц, ножно брать константу из config
    """
    root_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, "../..")))
    dir_path = os.path.join(root_dir, dir_name, year, month)

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    return dir_path


if __name__ == "__main__":
    pass
