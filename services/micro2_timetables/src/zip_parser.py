"""
Parse downloaded and readed .zip file
@M-Malek
"""


class ZIPParser:
    def __init__(self):
        pass
        # Main task: prepare data:
        # Idea: store data by line numbers (trip_id etc.)


"""
Dla każdej linii trzeba rozpisać dokładnie dane które potrzeba zapisać:
numer linii:
    id_przewoźnika: <value>,
    id_trasy:
        przebieg trasy:
            numer w sekwencji: nazwa_przystanku (id przystanku?), czas_przyjazdu, czas_odjazdu
Każda linia jako osobny .json?
"""
