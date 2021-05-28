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

    actual = pyfixedwidths.format(text)
    assert expected == actual
