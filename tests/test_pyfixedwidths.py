import pyfixedwidths
import pytest


@pytest.fixture(scope='function', autouse=False)
def sample_text1():
    text = (
        "1,2,3,4\n"
        "11,,33,44\n"
    )
    yield text


@pytest.fixture(scope='function', autouse=False)
def sample_text2():
    text = (
        "1\t2\t3\t4\n"
        "11\t\t33\t44\n"
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
        [1, None, 3, 4],
        [11, 22, None, 44],
    ]
    yield array


def test_usage(sample_dict1):
    fw = pyfixedwidths.FixedWidthFormatter()
    actual = fw.from_dict(sample_dict1).to_list()
    expect = [
        ["name      ", "age", "hobby", "job    "],
        ['John Doe  ', "20 ", 'swim ', '       '],
        ['John Smith', "100", '     ', 'teacher'],
    ]
    assert actual == expect


def test_from(sample_text1, sample_dict1, sample_array1):
    fw = pyfixedwidths.FixedWidthFormatter()
    fw.from_text(sample_text1)
    assert fw._rows == [
        ["1", "2", "3", "4"],
        ["11", "", "33", "44"],
    ]

    fw.from_dict(sample_dict1)
    assert fw._rows == [
        ["name", "age", "hobby", "job"],
        ['John Doe', "20", 'swim', ''],
        ['John Smith', "100", '', 'teacher'],
    ]

    fw.from_dict(sample_dict1, headers=["hobby", "job", "location", "name"])
    assert fw._rows == [
        ["hobby", "job", "location", "name"],
        ['swim', '', '', 'John Doe'],
        ['', 'teacher', '', 'John Smith'],
    ]

    fw.from_list(sample_array1)
    assert fw._rows == [
        ["1", "None", "3", "4"],
        ["11", "22", "None", "44"],
    ]


def test_from_text_with_sep(sample_text2):
    fw = pyfixedwidths.FixedWidthFormatter()
    fw.from_text(sample_text2, sep="\t")
    assert fw._rows == [
        ["1", "2", "3", "4"],
        ["11", "", "33", "44"],
    ]


def test_to(sample_dict1):
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
    assert fw.to_text(padding=1, end='', sep="\t") == (
        "name       \t age \t hobby \t job    \n"
        "John Doe   \t 20  \t swim  \t        \n"
        "John Smith \t 100 \t       \t teacher"
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


def test_to_with_schema2(sample_dict1):
    schema = [
        dict(
            justification='rjust'
        ),
        dict(
            format=':>5s'
        ),
        dict(
            min_width=1,
        ),
        dict(
            min_width=10,
            justification='rjust',
        )
    ]
    fw = pyfixedwidths.FixedWidthFormatter(schema=schema)
    fw.from_dict(sample_dict1)

    assert fw.to_list() == [
        ["      name", "  age", "hobby", "       job"],
        ['  John Doe', "   20", 'swim ', '          '],
        ['John Smith', "  100", '     ', '   teacher'],
    ]
    assert fw.to_text(padding=1) == (
        "      name ,   age , hobby ,        job\n"
        "  John Doe ,    20 , swim  ,           \n"
        "John Smith ,   100 ,       ,    teacher\n"
    )


def test_to_with_schema3():
    s = dict(
            min_width=2,
            width_calc_func=lambda width: width + -width % 3,
            justification='ljust',
        )
    schema = [ s, s, s, s, s, s, s ]
    array = [
        ['1', '12', '123', '1234', '12345', '123456', '1234567'],
    ]
    fw = pyfixedwidths.FixedWidthFormatter(schema=schema)
    fw.from_list(array)

    assert fw.to_list() == [
        ['1  ', '12 ', '123', '1234  ', '12345 ', '123456', '1234567  '],
    ]


def test_to_with_schema_error(sample_dict1):
    schema = [
        dict(
            min_width=1,
        ),
    ]
    fw = pyfixedwidths.FixedWidthFormatter(schema=schema)

    schema = [
        dict(
            min_width=1,
            format=':>5s',
        ),
    ]
    with pytest.raises(Exception):
        fw = pyfixedwidths.FixedWidthFormatter(schema=schema)

    schema = [
        dict(
            justification='rjust',
            format=':>1s'
        ),
    ]
    with pytest.raises(Exception):
        fw = pyfixedwidths.FixedWidthFormatter(schema=schema)


