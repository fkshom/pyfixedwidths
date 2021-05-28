__version__ = '0.1.0'

from pprint import pprint as pp

def format(text):
    def _column_width(rows):
        data_t = list(zip(*rows))
        widths = list(map(lambda val: len(val), [max(row, key=len) for row in data_t]))
        return widths

    lines = text.rstrip().split("\n")
    rows = [line.split(',') for line in lines]

    widths = _column_width(rows)
    pp(rows)
    results = []
    for row in rows:
        new_row = []
        for val, width in zip(row, widths):
            val = val.ljust(width)
            new_row.append(val)
        results.append(','.join(new_row))
    pp(results)
    return "\n".join(results) + "\n"

