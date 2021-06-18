class FixedWidthFormatter():
    def __init__(self, schema=None):
        if schema:
            for index in range(len(schema)):
                schema_formatting = schema[index].get('format')
                schema_justification = schema[index].get('justification')
                schema_min_width = schema[index].get('min_width', 0)
                schema_width_calc_func = schema[index].get('width_calc_func', None)

            if schema_formatting and (schema_justification or schema_min_width or schema_width_calc_func):
                raise Exception("Can not use justification or min_width, when use formatting.")

        self._schema = schema
        self._headers = None

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
            self._headers = headers

        _rows = []

        for row in rows:
            values = list(map(lambda header: row.get(header, ''), headers))
            _rows.append(values)
        return self.from_list(_rows)

    def from_list(self, rows, has_header=False, headers=None):
        import copy
        tmp = copy.deepcopy(rows)
        if has_header:
            self._headers = [str(val).strip() for val in tmp.pop(0)]
        if headers:
            self._headers = headers

        self._rows = [[str(val) for val in row] for row in tmp]
        return self

    def to_list(self, write_headers=True):
        def format_column_value(index, val, default_width):
            width = default_width
            justification = 'ljust'
            width_calc_func = lambda width: width
            formatting = None
            if self._schema:
                min_width = self._schema[index].get('min_width', 0)
                justification = self._schema[index].get('justification', justification)
                width_calc_func = self._schema[index].get('width_calc_func', width_calc_func)
                formatting = self._schema[index].get('format', formatting)

                width = max(int(width), int(min_width))
                width = width_calc_func(width)

            if formatting:
                val = ("{" + formatting + "}").format(val)
            else:
                justification_func = getattr(val, justification)
                val = justification_func(width)
            return val

        data = []
        if write_headers and self._headers:
            data.append(self._headers)
        data.extend(self._rows)
        widths = self._column_width(data)
        new_rows = []
        for row in data:
            new_row = []
            for index, (val, default_width) in enumerate(zip(row, widths)):
                val = format_column_value(index, val, default_width)
                new_row.append(val)
            new_rows.append(new_row)
        return new_rows

    def to_text(self, padding=1, end="\n", sep=","):
        new_rows = []
        sep = ' ' * padding + sep + ' ' * padding
        for row in self.to_list():
            new_rows.append(sep.join(row))
        return "\n".join(new_rows) + end

    def to_dict(self, write_header=True):
        if not self._headers:
            raise Exception("Headers not defined.")
        
        new_rows = []
        array = self.to_list()

        if not write_header:
            array.pop(0)
        for row in array:
            new_rows.append(dict(list(zip(self._headers, row))))
        return new_rows
