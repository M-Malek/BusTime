from ztm_tools.sorting.dates_sorting import data_range_sorter

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
    assert data_range_sorter("20260628", list4) == ("id_winner", "20260625-20260629"), "Test 4 failed"

    list5 = [("id_winner", "20260620-20260624"), ("id", "20260619-20260623"), ("id", "20260618-20260622")]

    assert data_range_sorter("20260620", list5) == ("id_winner", "20260620-20260624"), "Test 5 failed"

    list6 = [("id1", "20260618-20260626"), ("id2", "20260615-20260626"), ("id3", "20260612-20260627")]

    assert data_range_sorter("20260618", list6) == ("id1", "20260618-20260626"), "Test 6 failed"

    """
    All 6 tests passed!
    """