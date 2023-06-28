import os
import pytest
from GetCNNNews import GetNews, News
from project import Get_selectedFromList


@pytest.fixture
def input_getTopics():
    topics= [f"Toics{x}" for x in range(0,10)]
    return topics

#  test this using pytest .\test_project.py -k Get_selectedFromList -s  -v
def test_Get_selectedFromList(input_getTopics):
    x = 3
    header = ['Sr.No', 'Topics']
    print(len(input_getTopics))

    with pytest.raises(TypeError):
        Get_selectedFromList(input_getTopics)
    key = Get_selectedFromList(input_getTopics, header=header)
    assert len(input_getTopics) > key

# test this" pytest .\test_project.py -k systemExit -s  -v
def test_systemExit(input_getTopics):
    x = 3
    header = ['Sr.No', 'Topics']

    with pytest.raises(SystemExit) as pytest_wrapped_e:
            Get_selectedFromList(input_getTopics, header) <= 0 
    assert pytest_wrapped_e.type == SystemExit
