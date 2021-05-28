__version__ = '0.1.0'

from pprint import pprint as pp
from functools import reduce
def _column_width(rows):
    data_t = list(zip(*rows))
    widths = list(map(lambda val: len(val), [max(row, key=len) for row in data_t]))
    return widths

def format_dict(rows, padding=0):
    def extract_headers(dict_of_array):
        headers = [header for row in dict_of_array for header in row.keys()]
        headers = list({value: "" for value in headers})
        return headers
    headers = extract_headers(rows)

    _rows = []
    _rows.append(headers)

    for row in rows:
        values = list(map(lambda header: row.get(header, ''), headers))
        _rows.append(values)
    new_rows = format_array(_rows, padding=padding)
    return "\n".join(new_rows) + "\n"
    
def format_array(rows, padding=0):
    rows = [[str(val) for val in row] for row in rows]
    widths = _column_width(rows)
    pp(rows)
    new_rows = []
    for row in rows:
        new_row = []
        for val, width in zip(row, widths):
            val = val.ljust(width)
            new_row.append(val)
        new_rows.append((' ' * padding + ',' + ' ' * padding).join(new_row))
    pp(new_rows)
    return new_rows

def format_text(text, padding=0):
    lines = text.rstrip().split("\n")
    rows = [line.split(',') for line in lines]

    new_rows = format_array(rows, padding=padding)
    return "\n".join(new_rows) + "\n"
