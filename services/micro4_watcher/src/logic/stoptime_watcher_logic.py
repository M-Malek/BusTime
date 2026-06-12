"""
Raz na 3h sprawdzam sobie stronę ZTM -- jak wykryję zmiany w pliku to zapisuje nowy checksum i od kiedy ma on być
Jak sobie zapiszę to sprawdzam czy data od kiedy obowiązuje jest równa dacie dzisiejszej,
Jak jest rónwa dacie dzisiejszej to wysyłam o statystykę,
Jak zostanie zrobiona statystyka i dostanę zwrotną wiadomość SQS że jest zrobiona, to czyszczę sobie dane w S3 i
zapisuje nowe rozkłady jazdy
Watcher działa cały czas! sprawdza stronę ZTM, wystawia wiadomości o nowe dane i statystyke, pobiera od innych
informacje o stanie mikroserwisów
A ja zrobiłem że ma sprawdzić stronę i jak się coś zmieniło to se zmień :(
"""
from site_checking.ztm_site_checker import ztm_site_checker
from ztm_tools.logging import logger
from datetime import datetime

def ztm_watcher_logic():
    """
    Logic of ZTM site checking
    :return:
    """
    # Check ZTM site - look for new .zip file
    new_zip_data = ztm_site_checker()
    if new_zip_data:
        began_at = new_zip_data["began_at"]
        if began_at >= datetime.now().strftime("%Y%M%d"):
            logger("info", "New stop time data detected! From now!")
            # Add logic to set status "pending" of last entry in MongoDB as "actual"!
            return "data and statistic"
        else:
            logger("info", "New stop time data detected, pending in the future")
            return "statistic"
    else:
        logger("info", "No new ZTM file, statistic to do")
        return "statistic"