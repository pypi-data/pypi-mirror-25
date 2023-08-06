from terminaltables import SingleTable, AsciiTable
import sys
from commons import *
import pytz
import json


class Table:

    @staticmethod
    def new(format, columns):
        if format == 'json':
            return Json(columns)
        elif format == 'pretty':
            return Pretty(columns)
        else:
            return Simple(columns)

    def __init__(self, columns):
        self.columns = columns
        self.rows = [[c["name"] for c in self.columns]]
        self.items = []
        self.status = ""


    def humanize_bool(self, value):
        return TICK if value == "true" else CROSS


    def humanize(self, col, object):
        name = col["name"]
        if name not in object:
            return ""
        value = object[name]
        if "type" not in col:
            return value
        elif col["type"] is "size":
            return format_bytes(value)
        elif col["type"] is "number":
            return format_num(value)
        elif col["type"] is "boolean":
            return self.humanize_bool(value)
        elif col["type"] is "age":
            return format_seconds(value)

    def append(self, object):
        self.items.append(object)
        try:
            row = []
            for col in self.columns:
                row.append(self.humanize(col, object))
            self.rows.append(row)
        except Exception, e:
            import traceback
            traceback.print_exc(file=sys.stdout)

    def print_frame(self):
        pass

    def begin(self):
        pass

    def end(self):
        pass

    def update_status(self, status):
        self.status = status
        self.print_frame()


class Pretty(Table):
    def print_frame(self):
        sys.stdout.write(CLEAR_SCREEN + move_cursor(0, 0) + SingleTable(self.rows).table)
        sys.stdout.write("\n" + green(self.status + " ...\n"))


class Simple(Table):
    def print_frame(self):
        sys.stdout.write(AsciiTable(self.rows).table)


class Json(Table):

    def humanize_bool(self, value):
        return value

    def begin(self):
        sys.stdout.write("[")

    def end(self):
        sys.stdout.write("]")

    def print_frame(self):
        update_title(self.status)

    def append(self, object):
        row = {}
        for col in self.columns:
            row[col["name"]] = self.humanize(col, object)
        sys.stdout.write(json.dumps(row) + ",\n")
