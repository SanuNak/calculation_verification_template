from typing import Union

# В этом модуле можно также указать функции с лругими способами округлений

def school_round(a_in: Union[float, int],
                 n_in: int) -> Union[float, int]:
    """ Функция для округления математическим методом
    """
    if round((a_in * 10 ** (n_in + 1)) % 10, 5) == 5:
        return round(a_in + 1 / 10 ** (n_in + 1), n_in)
    else:
        return round(a_in, n_in)
