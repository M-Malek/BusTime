from src.mongo_service.mongo_iter_downloader import mongo_iter_downloader

def trips_data_importer(batch_count=100):
    mongo_iter_downloader("Poznan", "Line_info", batch_count)
