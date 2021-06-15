class FixedWidthFormatter():
    def __init__(self, schema=None):
        self._schema = schema

    def _column_width(self, rows):
        data_t = list(zip(*rows))
        widths = list(map(lambda val: len(val), [max(row, key=len) for row in data_t]))
        return widths

    def from_text(self, text, sep=","):
        lines = text.rstrip().split("\n")
        _rows = []
        for line in lines:
            vals = list(map(lambda val: val.strip(), line.split(sep)))
            _rows.append(vals)
        return self.from_list(_rows)

    def from_dict(self, rows, headers=None):
        def extract_headers(dict_of_array):
            headers = [header for row in dict_of_array for header in row.keys()]
            headers = list({value: "" for value in headers})
            return headers

        if not headers:
            headers = extract_headers(rows)

        _rows = []
        _rows.append(headers)

        for row in rows:
            values = list(map(lambda header: row.get(header, ''), headers))
            _rows.append(values)
        return self.from_list(_rows)

    def from_list(self, rows):
        self._rows = [[str(val) for val in row] for row in rows]
        return self

    def to_list(self):
        def format_column_value(index, val, width):
            if self._schema:
                schema_format = self._schema[index].get('format')
                schema_justification = self._schema[index].get('justification')
                if schema_format:
                    val = ("{" + schema_format + "}").format(val)
                elif schema_justification:
                    justification_func = getattr(val, schema_justification)
                    val = justification_func(width)
                else:
                    val = val.ljust(width)
            else:
                val = val.ljust(width)
            return val

        widths = self._column_width(self._rows)
        new_rows = []
        for row in self._rows:
            new_row = []
            for index, (val, width) in enumerate(zip(row, widths)):
                val = format_column_value(index, val, width)
                new_row.append(val)
            new_rows.append(new_row)
        return new_rows

    def to_text(self, padding=1, end="\n", sep=","):
        new_rows = []
        sep = ' ' * padding + sep + ' ' * padding
        for row in self.to_list():
            new_rows.append(sep.join(row))
        return "\n".join(new_rows) + end
