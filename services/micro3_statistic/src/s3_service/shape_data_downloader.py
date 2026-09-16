from ztm_tools.s3_manager.download_data.file_downloader import download_data_shapes
from ztm_tools.models.shape import ReadyShape

def download_shape_data(shape_id):
    """
    Download the shape data from S3
    :param shape_id: str, shape_id of the shape
    :return: data for given shape as Shape
    """
    raw_shape_data = download_data_shapes(shape_id)
