class Schema():
    def __init__(self, default={}):
        self._default_schema_item = dict(
            format=None,
            justification='ljust',
            min_width=0,
            width_calc_func=lambda width: width,
        )
        self._default_schema_item = self._default_schema_item.update(default)
        self._schema = dict()

    def validate_schema(self, schema_dict):
        schema_formatting = schema_dict.get('format')
        schema_justification = schema_dict.get('justification')
        schema_min_width = schema_dict.get('min_width', 0)
        schema_width_calc_func = schema_dict.get('width_calc_func', None)

        if schema_formatting and (schema_justification or schema_min_width or schema_width_calc_func):
            raise Exception("Can not use justification or min_width, when use formatting.")
    
    def set_schema(self, schema):
        if not schema:
            return
        
        if type(schema) is list:
            for index in range(len(schema)):
                self.validate_schema(schema[index])
            self._schema = dict(zip(list(range(len(schema))), schema))
        elif type(schema) is dict:
            for key in list(schema.keys()):
                self.validate_schema(schema[key])
            self._schema = schema
        else:
            raise Exception(f"schema must be list or dict. {type(schema)}")

    def get_schema(self, index_or_key):
        return self._schema.get(index_or_key, self._default_schema_item)

    def format_column_value(self, index_or_key, val, default_width):
        width = default_width
        justification = 'ljust'
        width_calc_func = lambda width: width
        formatting = None
        if self._schema:
            min_width = self.get_schema(index_or_key).get('min_width', 0)
            justification = self.get_schema(index_or_key).get('justification', justification)
            width_calc_func = self.get_schema(index_or_key).get('width_calc_func', width_calc_func)
            formatting = self.get_schema(index_or_key).get('format', formatting)

            width = max(int(width), int(min_width))
            width = width_calc_func(width)

        if formatting:
            val = ("{" + formatting + "}").format(val)
        else:
            justification_func = getattr(val, justification)
            val = justification_func(width)
        return val

class FixedWidthFormatter():
    def __init__(self, schema=None):
        self._schema = Schema()
        self._schema.set_schema(schema)
        self._headers = None
        self._rows = []

    def from_dict(self, array_of_dict, headers=None):
        def extract_headers(array_of_dict):
            headers = [header for row in array_of_dict for header in row.keys()]
            headers = list({value: "" for value in headers})
            return headers

        if not headers:
            headers = extract_headers(array_of_dict)
            self._headers = headers
            self._valid_header = True

        self._rows = array_of_dict
        return self

    def from_list(self, array_of_array, has_header=False, headers=None):
        import copy
        tmp = copy.deepcopy(array_of_array)
        if has_header:
            headers = [str(val).strip() for val in tmp.pop(0)]

        if not headers:
            headers = list(range(len(tmp[0])))

        self.from_dict(dict(zip(headers, tmp)), headers)
        return self

    def from_text(self, text, sep=",", has_header=False):
        lines = text.rstrip().split("\n")
        _rows = []
        for line in lines:
            vals = list(map(lambda val: val.strip(), line.split(sep)))
            _rows.append(vals)
        return self.from_list(_rows, has_header)


    def to_list(self, write_headers=True):
        data = []
        if write_headers and self._headers:
            data.append(self._headers)
        for row in self._rows:
            data.append(list(map(lambda header: row[header]), self._headers))

        widths = self._column_width(data)
        new_rows = []
        for row in data:
            new_row = []

            for index_or_key, (val, default_width) in self._
            if not self._schema or type(self._schema) is list:            
                for index, (val, default_width) in enumerate(zip(row, widths)):
                    val = format_column_value(index, val, default_width)
                    new_row.append(val)
            elif self._headers and type(self._schema) is dict:
                for key, val, default_width in zip(self._headers, row, widths):
                    val = format_column_value(key, val, default_width)
                    new_row.append(val)

            new_rows.append(new_row)
        return new_rows

class FixedWidthFormatter_():
    def __init__(self, schema=None):
        def validate_schema(schema_dict):
            schema_formatting = schema_dict.get('format')
            schema_justification = schema_dict.get('justification')
            schema_min_width = schema_dict.get('min_width', 0)
            schema_width_calc_func = schema_dict.get('width_calc_func', None)

            if schema_formatting and (schema_justification or schema_min_width or schema_width_calc_func):
                raise Exception("Can not use justification or min_width, when use formatting.")

        if schema and type(schema) is list:
            self._schema = schema
            for index in range(len(schema)):
                validate_schema(schema[index])
        elif schema and type(schema) is dict:
            self._schema = schema
            for key in list(schema.keys()):
                validate_schema(schema[key])
        elif not schema:
            self._schema = None
        else:
            raise Exception(f"schema must be list or dict. {type(schema)}")

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

        # self._rows = [[str(val) for val in row] for row in tmp]
        indexes = list(range(len(self._rows[0])))
        self._rows = dict(zip(indexes, self._rows))
        return self

    def get_schema(self, index_or_key):
        if type(self._schema) is list:
            return self._schema[index_or_key]
        elif type(self._schema) is dict:
            return self._schema.get(index_or_key, {})

    def to_list(self, write_headers=True):
        def format_column_value(index_or_key, val, default_width):
            width = default_width
            justification = 'ljust'
            width_calc_func = lambda width: width
            formatting = None
            if self._schema:
                min_width = self.get_schema(index_or_key).get('min_width', 0)
                justification = self.get_schema(index_or_key).get('justification', justification)
                width_calc_func = self.get_schema(index_or_key).get('width_calc_func', width_calc_func)
                formatting = self.get_schema(index_or_key).get('format', formatting)

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

            if not self._schema or type(self._schema) is list:            
                for index, (val, default_width) in enumerate(zip(row, widths)):
                    val = format_column_value(index, val, default_width)
                    new_row.append(val)
            elif self._headers and type(self._schema) is dict:
                for key, val, default_width in zip(self._headers, row, widths):
                    val = format_column_value(key, val, default_width)
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
