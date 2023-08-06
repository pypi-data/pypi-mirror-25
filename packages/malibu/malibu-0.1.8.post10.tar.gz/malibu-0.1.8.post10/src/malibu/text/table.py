# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import math
import types

from malibu.text import (
    string_type,
    unicode_type
)


class ObjectTable(object):

    TABLE_CORNER = "+"
    TABLE_VBORDER = "|"
    TABLE_HBORDER = "-"

    def __init__(self, obj, max_width=-1, delimit_cells=False, title=None,
                 render_subtables=False, subtable_depth=1):

        if max_width == 0 or not max_width:
            max_width = 78

        self.max_width = max_width
        self.actual_width = max_width
        self._title = title
        self._delimit_cells = delimit_cells
        self._render_subtables = render_subtables
        self._subtable_depth = subtable_depth

        self._max_key_col_width = None
        self._max_val_col_width = None

        if isinstance(obj, dict):
            self._obj = obj.copy()
        else:
            # `obj` can also be any type of object, as long as it has a function
            # `as_dict() -> dict(...)`.
            if not hasattr(obj, 'as_dict'):
                raise TypeError('%s has no `as_dict` function/method' % (obj))

            attr = getattr(obj, 'as_dict')
            if type(attr) not in [
                                    types.FunctionType,
                                    types.MethodType,
                                    types.LambdaType
                                 ]:
                raise AttributeError('%s.as_dict is not a function/method' % (
                    obj
                ))
            else:
                _obj = obj.as_dict()
                if not isinstance(_obj, dict):
                    raise TypeError('%s.as_dict does not return a dict' % (obj))
                self._obj = _obj

        self._obj = self.__stringify_dict(self._obj)

    def __len__(self):
        """ Returns the actual width (length) of the table.
        """

        return self.actual_width + 2

    def __stringify_dict(self, d):
        """ Turns all values in a dict into strings.
            If `render_subtables` is set, dictionary values will not be
            stringified.
        """

        conv = d.copy()

        for k, v in conv.copy().items():
            if isinstance(v, dict) and self._render_subtables:
                continue

            conv.update({
                k: str(v),
            })

        return conv

    def __recurse_subtables(self):
        """ Creates all subtables from nested dictionaries.

            Subtables will inherit all properties from the parent table except
            for the title and max_width.
        """

        if self._subtable_depth == 0:
            return

        for k, v in self._obj.copy().items():
            if isinstance(v, dict):
                st = ObjectTable(
                    v,
                    delimit_cells=self._delimit_cells,
                    render_subtables=self._render_subtables,
                    subtable_depth=self._subtable_depth - 1
                )

                # Do the rendering calculations on the subtable
                st._ObjectTable__recurse_subtables()
                st._ObjectTable__render_body(calculate_only=True)

                self._obj.update({
                    k: st,
                })

        self.__render_body(calculate_only=True)

    def set_title(self, s):
        """ Sets the table title.
        """

        self._title = s

    def __render_title(self):
        """ Renders the title block.
        """

        if not self._title:
            return

        title_text = self.__wrap(self._title, self.actual_width)
        rendered = []

        rendered.append(self.__render_border(self.actual_width))
        for line in title_text:
            rendered.append(
                ("{:s}{:^%d}{:s}" % (self.actual_width)).format(
                    self.TABLE_VBORDER,
                    line.strip(),
                    self.TABLE_VBORDER
                )
            )

        return rendered

    def __wrap(self, text, length, keep_pad=True):
        """ Wraps a string to the specified length.
            Will return a list with the string wrapped to length.
        """

        if len(text) > length:
            pad = length * int(math.ceil(len(text) / float(length))) - len(text)
            text = text + ' ' * pad
        elif len(text) < length:
            pad = length - len(text)
            text = text + ' ' * pad

        wrapped = []
        wrapped.extend(zip(*[
            text[i::length] for i in range(0, length)]
        ))

        lines = []
        for line in wrapped:
            lines.append(''.join(line))

        if not keep_pad:
            lines[-1] = lines[-1].rstrip()

        return lines

    def __pad_right(self, s, length, char=' '):
        """ Pads a string up to length on the right side.
        """

        if type(s) not in [string_type(), unicode_type()]:
            raise TypeError('s must be a string')

        slen = len(s)
        pad_len = length - slen
        if pad_len <= 0:
            return s

        return s + (char * pad_len)

    def __render_border(self, length):
        """ Renders a border with corners.
        """

        return "%s%s%s" % (
            self.TABLE_CORNER,
            self.TABLE_HBORDER * (length),
            self.TABLE_CORNER
        )

    def __render_delimiter(self, key_len, val_len):
        """ Renders the cell separator / delimiter.
        """

        return "%s%s%s%s%s" % (
            self.TABLE_CORNER,
            self.TABLE_HBORDER * (key_len),
            self.TABLE_CORNER,
            self.TABLE_HBORDER * (val_len),
            self.TABLE_CORNER
        )

    def __render_body(self, calculate_only=False):
        """ Renders the body of the table. It's useful to do this first so we
            know the "actual" rendered width of the table after text wrapping
            has been applied.

            Best way to do this:
                1. Iterate through keys to find the best-fit value for the
                   key column.
                2. Iterate through values to find the best-fit value for the
                   value column, which *absolutely* must not exceed
                   `max_width - key_col_width`.
                3. Add the values from [1] and [2] to get the "actual" table
                   width.
                4. Render cells individually. A cell is a single key-value pair
                   which may or may not wrap around to the next line.
        """

        # Find the max key/val lengths
        max_key_len = max(map(lambda i: len(i), self._obj.keys()))
        max_val_len = max(map(lambda i: len(i), self._obj.values()))

        # Calculate "actual" width
        sep_len = (len(self.TABLE_VBORDER) * 3) + 2
        self.actual_width = max_key_len + max_val_len + sep_len
        if self.max_width == -1:
            self.max_width = self.actual_width

        # Ensure key and value sizes, with separators, don't exceed max_width
        if self.max_width != -1 and self.actual_width > self.max_width:
            max_val_len = self.max_width - max_key_len - sep_len
            self.actual_width = max_key_len + max_val_len + sep_len

        if calculate_only:
            self._max_key_col_width = max_key_len
            self._max_val_col_width = max_val_len

            return []

        cells = []
        for k, v in self._obj.items():
            k = self.__wrap(k, max_key_len)
            if isinstance(v, list):
                v = str(v)

            if type(v) in [string_type(), unicode_type()]:
                v = self.__wrap(v, max_val_len)
            elif self._render_subtables and isinstance(v, ObjectTable):
                v = [self.__pad_right(s, max_val_len) for s in v.render()]

            if len(k) > len(v):
                while len(v) != len(k):
                    v.append(' ' * max_val_len)
            elif len(k) < len(v):
                while len(k) != len(v):
                    k.append(' ' * max_key_len)

            cells.append((k, v,))

        rendered_cells = []
        rendered_cells.append(self.__render_delimiter(
            max_key_len + 2,
            max_val_len + 2
        ))

        # Render body cells
        for cell_keys, cell_vals in cells:
            for key, value in zip(cell_keys, cell_vals):
                rendered_cells.append("%s %s %s %s %s" % (
                    self.TABLE_VBORDER,
                    key,
                    self.TABLE_VBORDER,
                    value,
                    self.TABLE_VBORDER
                ))

            if self._delimit_cells:
                rendered_cells.append(self.__render_delimiter(
                    max_key_len + 2,
                    max_val_len + 2
                ))

        if not self._delimit_cells:
            # If cells are being delimited, the final line will already
            # be printed when this happens.
            rendered_cells.append(self.__render_delimiter(
                max_key_len + 2,
                max_val_len + 2
            ))

        return rendered_cells

    def render(self):
        """ Renders the object table. The reference object should be stored in
            `self._obj` and should *only* be a dictionary.

            The rendered table will look like this:

                +---------------------------------+
                |   ... title data, if given ...  |
                +-----+---------------------------+
                | key | value info......          |
                | ... | ...                       |
                +-----+---------------------------+
        """

        cells = []
        if self._obj and self._title:
            self.__render_body(calculate_only=True)

        if self._render_subtables:
            self.__recurse_subtables()

        self._prerender_obj = self._obj.copy()

        if self._title:
            cells.extend(self.__render_title())

        if self._obj:
            cells.extend(self.__render_body())

        return cells

    def print_table(self):
        """ Takes the rendered output and prints it directly to the screen.
        """

        for cell in self.render():
            print(cell)


class TextTable(object):

    TABLE_CORNER = "+"
    TABLE_VT_BORDER = "|"
    TABLE_HZ_BORDER = "-"

    def __init__(self, min_width=12):

        self.min_width = min_width

        self._rows = 0
        self._columns = 0

        # Header data should be simple; it should be no more than a list of
        # strings naming each column header.
        self._header_data = []

        # Row data should be internally stored in a zipped-set form, or, as a
        # list of tuples, which each tuple containing all the entries for a
        # single row.
        self._row_data = []

    def add_header_list(self, el):

        if not isinstance(el, list):
            return

        self._columns = len(el)
        self._header_data = el

    def add_header(self, *args):

        self._columns = len(args)
        self._header_data = [arg for arg in args]

    def add_data_dict(self, el):
        """ add_data_dict only really makes sense to use when there is a
            single pair mapping (eg., key, value) or a two column
            display.  If that is not that case, add_data_ztup is a better
            choice.
        """

        if not isinstance(el, dict):
            return

        self._rows = len(el)

        for key, value in el.items():
            self._row_data.append((key, value,))

    def add_data_ztup(self, el):
        """ add_data_ztup will take any as much data as you need and can even
            fill the place of add_data_dict.  add_data_ztup takes a list of
            tuples. each tuple should contain a row of elements, one element
            for each column. essentially, the argument that will be passed
            in should look like:
              [
                (x1, y1, z1),
                (x2, y2, z2),
                    ...
                (xn, yn, zn)
              ]
        """

        if not isinstance(el, list):
            return

        self._rows = len(el)

        for row in el:
            row = [str(item) for item in row]
            if len(row) > self._columns:
                row = row[0:self._columns - 1]
            elif len(row) < self._columns:
                col_diff = (self._columns - len(row)) + 1
                col_fill = len(row)
                for idx in range(col_fill, col_diff):
                    el[idx] = ''
            self._row_data.append(row)

    def add_data_kv(self, k, v):
        """ add_data_kv is a simplified add_data_dict for pushing a data pair onto the
            row list on-the-fly. only effective for two-column data sets.
        """

        self._row_data.append((k, v,))

    def add_data_list(self, el):
        """ add_data_list adds a list of data to the table. this is primarily
            suitable for single-column data sets.
        """

        [self._row_data.append((elm,)) for elm in el]

    def add_data_csv_file(self, fobj):
        """ add_data_csv_file loads data from a comma-separated value file.
            the first row is the header, everything else is actual data.
            works if the file is provided or if a string containing the
            filename is given.
        """

        if isinstance(fobj, str):
            try:
                fobj = io.open(fobj, 'r')
            except:
                raise

        data_flag = False

        for line in fobj.readlines():
            line = line.strip().split(",")
            if not data_flag:
                self._columns = len(line)
                self.add_header(*line)
                data_flag = True
                continue
            self._row_data.append(tuple(line))

    def __transpose_list(self, li):
        """ Performs a simple transposition on a list.
            Used for calculating row sizes and maxes.
        """

        return map(list, zip(*li))

    def __calculate_row_max(self):
        """ Calculates the max size of the rows so the table can uniformly
            render all the columns.
        """

        __sizes = []

        for row in self._row_data:
            __sizes.append([len(el) for el in row])

        __sizes = self.__transpose_list(__sizes)

        return [max(cols) for cols in __sizes]

    def __format_divider(self):
        """ Returns the table divider.
        """

        s = ""
        col_sizes = self.__calculate_row_max()

        for size in col_sizes:
            s += TextTable.TABLE_CORNER
            if size >= self.min_width:
                s += (TextTable.TABLE_HZ_BORDER * (size + 2))
            else:
                s += (TextTable.TABLE_HZ_BORDER * self.min_width)
        s += TextTable.TABLE_CORNER

        return s

    def __pad_left(self, txt, length):
        """ Pads a string to be `length` characters long, from left.
        """

        s = []

        if len(txt) < length:
            diff = length - len(txt) - 1
            [s.append(" ") for i in range(0, diff)]
            s.append(''.join(txt) + " ")
        elif len(txt) == length:
            s.append(txt)

        return ''.join(s)

    def __format_header_data(self):
        """ Formats the header data.
        """

        lines = []
        col_sizes = self.__calculate_row_max()

        line = ""

        cd = zip(self._header_data, col_sizes)
        for (text, size) in cd:
            if size < self.min_width:
                size = self.min_width
            elif size >= self.min_width:
                size = size + 2
            text = self.__pad_left(text, size)
            line += TextTable.TABLE_VT_BORDER
            line += text
        line += TextTable.TABLE_VT_BORDER
        lines.append(line)

        return lines

    def __format_table_data(self):
        """ Formats the table data.
        """

        lines = []
        col_sizes = self.__calculate_row_max()

        for row in self._row_data:
            rd = zip(row, col_sizes)
            line = ""
            for (text, size) in rd:
                if size < self.min_width:
                    size = self.min_width
                elif size >= self.min_width:
                    size = size + 2
                text = self.__pad_left(text, size)
                line += TextTable.TABLE_VT_BORDER
                line += text
            line += TextTable.TABLE_VT_BORDER
            lines.append(line)

        return lines

    def format(self):
        """ Format the table and return the string.
        """

        if len(self._row_data) == 0:
            return None

        lines = []
        divider = self.__format_divider()

        lines.append(divider)
        [lines.append(line) for line in self.__format_header_data()]
        lines.append(divider)
        [lines.append(line) for line in self.__format_table_data()]
        lines.append(divider)

        return lines
