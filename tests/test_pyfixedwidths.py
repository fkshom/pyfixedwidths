from pyfixedwidths import __version__
import pyfixedwidths


def test_version():
    assert __version__ == '0.1.0'


def test_run():
    text = (
        "1,2,3,4\n"
        "11,22,33,44\n"
    )

    expected = (
        "1 ,2 ,3 ,4 \n"
        "11,22,33,44\n"
    )

    actual = pyfixedwidths.format_text(text)
    assert expected == actual

def test_run2():
    text = (
        "1,2,3,4\n"
        "11,22,33,44\n"
    )

    expected = (
        "1  , 2  , 3  , 4 \n"
        "11 , 22 , 33 , 44\n"
    )

    actual = pyfixedwidths.format_text(text, padding=1)
    assert expected == actual

def test_run3():
    origin = [
        dict(
            firstname='Taro',
            lastname='Tanaka',
            age=20,
            flag=True,
            job='Student'
        ),
        dict(
            firstname='Hanako',
            lastname='Suzuki',
            age=18,
            flag=False,
            hobby='Music'
        )
    ]

    expected = (
        "firstname , lastname , age , flag  , job     , hobby\n"
        "Taro      , Tanaka   , 20  , True  , Student ,      \n"
        "Hanako    , Suzuki   , 18  , False ,         , Music\n"
    )

    actual = pyfixedwidths.format_dict(origin, padding=1)
    assert expected == actual
