from src.mongo_service.mongo_iter_downloader import mongo_iter_downloader
from ztm_tools.models.trip_progress import TripProgress

def trips_data_importer(batch_count=100):
    """Return every saved line-info document as a ``TripProgress`` object."""
    documents = mongo_iter_downloader("Poznan", "Line_info", batch_count)
    return [TripProgress.from_dict(document) for document in documents]
