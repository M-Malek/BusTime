from ztm_tools.sorting.dates_sorting import data_range_sorter
from bson.objectid import ObjectId

def test_data_range_sorter():
    # Example 1: 4 different ranges:
    list1 = [("id", "20260614-20260622"), ("id", "20260609-20260609"), ("id_winner", "20260611-20260616"),
                                                                      ("id", "20260607-20260630")]

    assert data_range_sorter("20260612", list1) == ("id_winner", "20260611-20260616"), "Test 1 failed"

    # Example 2: 4 different ranges with the same beginning date:
    list2 = [("id", "20260609-20260622"), ("id_winner", "20260609-20260610"), ("id", "20260609-20260616"),
             ("id", "20260609-20260630")]

    # print(data_range_sorter("20260610", list2))
    assert data_range_sorter("20260610", list2) == ("id_winner", "20260609-20260610"), "Test 2 failed"

    # Example 3: 4 different ranges which are almost the same (two identical):
    list3 = [("id_1_idi", "20260609-20260610"), ("id", "20260609-20260611"), ("id_2_idi", "20260609-20260610"),
             ("id_winner", "20260609-20260609")]

    assert data_range_sorter("20260609", list3) == ("id_winner", "20260609-20260609"), "Test 3 failed"

    # Example 4: situation when new month begins:
    list4 = [("id_winner", "20260625-20260629"), ("id", "20260627-20260703"), ("id", "20260625-20260630")]

    # print(data_range_sorter("20260628", list4))
    assert data_range_sorter("20260628", list4) == ("id","20260627-20260703"), "Test 4 failed"

    list5 = [("id_winner", "20260620-20260624"), ("id", "20260619-20260623"), ("id", "20260618-20260622")]

    assert data_range_sorter("20260620", list5) == ("id_winner", "20260620-20260624"), "Test 5 failed"

    list6 = [("id1", "20260618-20260626"), ("id2", "20260615-20260626"), ("id3", "20260612-20260627")]

    assert data_range_sorter("20260618", list6) == ("id1", "20260618-20260626"), "Test 6 failed"

    list7 = [(ObjectId('6a57ac2ca0da0cccb4f07cc5'), '20260716-20260726'),
             (ObjectId('6a592da7c6fc3451a5176818'), '20260717-20260726'),
             (ObjectId('6a5cede57c143b32badf4d82'), '20260718-20260726'),
             (ObjectId('6a5fa621502db0d8d2049424'), '20260722-20260726'),
             (ObjectId('6a62667a1e2d0a43843aee05'), '20260724-20260726'),
             (ObjectId('6a74d263be3aed517a24518d'), '20260801-20260807'),
             (ObjectId('6a74d264be3aed517a24518f'), '20260729-20260731'),
             (ObjectId('6a74d264be3aed517a245190'), '20260727-20260731'),
             (ObjectId('6a7b595436242a9819c5bb08'), '20260810-20260823'),
             (ObjectId('6a7b595436242a9819c5bb09'), '20260806-20260816'),
             (ObjectId('6a7b595536242a9819c5bb0a'), '20260730-20260731')]
    assert data_range_sorter("20260811", list7) == (ObjectId('6a7b595436242a9819c5bb08'), '20260810-20260823'), "Test 7 failed"
    """
    All 6 tests passed!
    """