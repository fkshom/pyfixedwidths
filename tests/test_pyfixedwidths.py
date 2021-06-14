from pyfixedwidths import __version__
import pyfixedwidths

import pytest

def test_version():
    assert __version__ == '0.1.0'

@pytest.fixture(scope='function', autouse=False)
def sample_text1():
    text = (
        "1,2,3,4\n"
        "11,22,33,44\n"
    )
    yield text

@pytest.fixture(scope='function', autouse=False)
def sample_dict1():
    listofdict = [
        dict(name="John Doe", age=20, hobby="swim"),
        dict(name="John Smith", age=100, job="teacher"),
    ]
    yield listofdict

@pytest.fixture(scope='function', autouse=False)
def sample_array1():
    array = [
        [1,None,3,4],
        [11,22,None,44],
    ]
    yield array

def test_from(sample_text1, sample_dict1, sample_array1):
    fw = pyfixedwidths.FixedWidthFormatter()
    fw.from_text(sample_text1)
    assert fw._rows == [
        ["1", "2", "3", "4"],
        ["11", "22", "33", "44"],
    ]

    fw.from_dict(sample_dict1)
    assert fw._rows == [
        ["name", "age", "hobby", "job"],
        ['John Doe', "20", 'swim', ''],
        ['John Smith', "100", '', 'teacher'],
    ]

    fw.from_list(sample_array1)
    assert fw._rows == [
        ["1" , "None", "3", "4"],
        ["11", "22", "None", "44"],
    ]

def test_to(sample_dict1):
    expected = [
        ["1  ", " None ", " 3    ", " 4  "],
        ["11 ", " 22   ", " None ", " 44 "],
    ]
    fw = pyfixedwidths.FixedWidthFormatter()
    fw.from_dict(sample_dict1)
    
    assert fw.to_list() == [
        ["name      ", "age", "hobby", "job    "],
        ['John Doe  ', "20 ", 'swim ', '       '],
        ['John Smith', "100", '     ', 'teacher'],
    ]
    assert fw.to_text(padding=0) == (
        "name      ,age,hobby,job    \n"
        "John Doe  ,20 ,swim ,       \n"
        "John Smith,100,     ,teacher\n"
    )
    assert fw.to_text(padding=1, end='') == (
        "name       , age , hobby , job    \n"
        "John Doe   , 20  , swim  ,        \n"
        "John Smith , 100 ,       , teacher"
    )

def test_to_with_schema(sample_dict1):
    schema = [
        dict(
            justification='rjust'
        ),
        dict(
            format=':>5s'
        ),
        dict(),
        dict(
            format=':2s'
        )
    ]
    fw = pyfixedwidths.FixedWidthFormatter(schema=schema)
    fw.from_dict(sample_dict1)

    assert fw.to_list() == [
        ["      name", "  age", "hobby", "job"],
        ['  John Doe', "   20", 'swim ', '  '],
        ['John Smith', "  100", '     ', 'teacher'],
    ]
    assert fw.to_text(padding=1) == (
        "      name ,   age , hobby , job\n"
        "  John Doe ,    20 , swim  ,   \n"
        "John Smith ,   100 ,       , teacher\n"
    )

# def test_run4():
#     schema = dict(
#         age=dict(
#             justification='rjust',
#         )
#     )
#     origin = [
#         dict(
#             firstname='Taro',
#             lastname='Tanaka',
#             age=20,
#             flag=True,
#             job='Student'
#         ),
#         dict(
#             firstname='Hanako',
#             lastname='Suzuki',
#             age=18,
#             flag=False,
#             hobby='Music'
#         )
#     ]

#     expected = (
#         "firstname , lastname , age , flag  , job     , hobby\n"
#         "Taro      , Tanaka   ,  20 , True  , Student ,      \n"
#         "Hanako    , Suzuki   ,  18 , False ,         , Music\n"
#     )

#     actual = pyfixedwidths.format_dict(origin, padding=1, schema=schema)
#     assert expected == actual
