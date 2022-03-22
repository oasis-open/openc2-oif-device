import re

from typing import Any, Sequence, Tuple, Union
from osquery.extension_client import Client
from osquery.extensions.ttypes import ExtensionResponse
from peewee import DatabaseError, InterfaceError, ProgrammingError

PY_CHARSET = "UTF-8"
RE_PY_PARAM = re.compile(b'\?')
RE_PY_MAPPING_PARAM = re.compile(
    br'''
    %
    \((?P<mapping_key>[^)]+)\)
    (?P<conversion_type>[diouxXeEfFgGcrs%])
    ''', re.X)


class _ParamSubstitutor:
    def __init__(self, params):
        self.params = params
        self.index = 0

    def __call__(self, matchobj):
        index = self.index
        self.index += 1
        try:
            return bytes(self.params[index])
        except IndexError:
            raise ProgrammingError("Not enough parameters for the SQL statement")

    @property
    def remaining(self):
        return len(self.params) - self.index


def _bytestr_format_dict(bytestr, value_dict):
    def replace(matchobj):
        value = None
        groups = matchobj.groupdict()
        if groups["conversion_type"] == b"%":
            value = b"%"
        if groups["conversion_type"] == b"s":
            key = groups["mapping_key"]
            value = value_dict[key]
        if value is None:
            raise ValueError(f"Unsupported conversion_type: {groups['conversion_type']}")
        return value
    return RE_PY_MAPPING_PARAM.sub(replace, bytestr)


class OSQueryCursor:
    """
    Implements the Python Database API Specification v2.0 (PEP-249)
    """
    _arraysize: int = 1
    _commit: bool
    _executed: Union[bytes,str]
    _index: int
    _lastrowid: Any
    _rowcount: int
    _stored_results: list
    # tuple of column names, 7-tuple per column
    _description: Tuple[Tuple[str, None, None, None, None, None, None], ...] = None
    _connection: Client

    def __init__(self, commit: bool = False):
        # Custom Props
        self._nextrow = None
        self._rowcount = 0
        self._commit = commit
        self._fetchcount = -1
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row = self.fetchone()
        except InterfaceError:
            raise StopIteration
        if not row:
            raise StopIteration
        return row

    def close(self):
        if self._connection is None:
            return False

        self._reset_result()
        self._connection = None
        return True

    def execute(self, sql: str, params: tuple = ()):
        self._reset_result()
        stmt = sql if isinstance(sql, (bytes, bytearray)) else sql.encode(PY_CHARSET)
        if params:
            if isinstance(params, dict):
                stmt = _bytestr_format_dict(sql, self._process_params_dict(params))
            elif isinstance(params, (list, tuple)):
                psub = _ParamSubstitutor(self._process_params(params))
                stmt = RE_PY_PARAM.sub(psub, stmt)
                if psub.remaining != 0:
                    raise ProgrammingError(f"Not all parameters were used in the SQL statement: {psub.remaining}")

        table_name = stmt.split(b"FROM")[1].split(b"AS")[0].strip(b" \"").decode(PY_CHARSET)
        self._handle_pragma(self._connection.query(f"PRAGMA table_info({table_name})"))
        self._handle_result(self._connection.query(stmt.decode(PY_CHARSET)))
        return self._stored_results

    def executemany(self, sql: str, params: Tuple[tuple] = ()):
        print('executemany')
        results = []
        for param in params:
            results.append(self.execute(sql, param))
        print(f'-- {results}')

    def executescript(self, sql: str):
        """Executes a multiple SQL statements at once. Non-standard"""
        print('executescript')

    def fetchone(self):
        return self._fetch_row()

    def fetchmany(self, size: int = 0):  # def fetchmany(self, size=cursor.arraysize):
        return self._stored_results[:size or self._arraysize] or None

    def fetchall(self):
        return self._stored_results or None

    # Properties
    rowcount = property(lambda self: self._rowcount, lambda self, v: setattr(self, '_rowcount', v))
    lastrowid = property(lambda self: self._lastrowid, lambda self, v: None)
    arraysize = property(lambda self: self._arraysize, lambda self, v:  setattr(self, '_arraysize', v))
    description = property(lambda self: self._description, lambda self, v: None)
    connection = property(lambda self: self._connection, lambda self, v: None)
    # row_factory = property(lambda self: object(), lambda self, v: None)

    # Customizations
    def __str__(self):
        fmt = "{class_name}: {stmt}"
        if self._executed:
            try:
                executed = self._executed.decode('utf-8')
            except AttributeError:
                executed = self._executed
            if len(executed) > 40:
                executed = executed[:40] + '..'
        else:
            executed = '(Nothing executed yet)'
        return fmt.format(class_name=self.__class__.__name__, stmt=executed)

    def _handle_pragma(self, pragma: ExtensionResponse):
        def column(col: str) -> Tuple[str, None, None, None, None, None, None]:
            return col, None, None, None, None, None, None

        if not isinstance(pragma, ExtensionResponse):
            raise InterfaceError('Result was not an ExtensionResponse')
        columns = []
        for col in pragma.response:
            columns.append(col["name"])
        self._description = tuple(map(column, columns))

    def _handle_result(self, result: ExtensionResponse):
        if not isinstance(result, ExtensionResponse):
            raise InterfaceError('Result was not an ExtensionResponse')

        if result.status.code != 0:
            raise DatabaseError(result.status.message)
        self._rowcount = len(result.response)
        columns = set(c for r in result.response for c in r.keys())
        self._description = tuple(d for d in self._description if d[0] in columns)
        self._stored_results = [[r.get(d[0]) for d in self._description] for r in result.response]

    def _fetch_row(self):
        if self._fetchcount == len(self._stored_results):
            return None

        if self._nextrow is None and len(self._stored_results) == 0:
            return None
        elif self._nextrow is None:
            row = self._stored_results[0]
        else:
            row = self._nextrow

        if row:
            self._nextrow = self._stored_results[self._fetchcount]
            if self._fetchcount == -1:
                self._fetchcount = 1
            else:
                self._fetchcount += 1
        return row

    def _reset_result(self):
        self._index = 0
        self._rowcount = -1
        self._fetchcount = -1
        self._nextrow = None
        self._stored_results = []
        self._description = None
        self._executed = None

    def _process_params_dict(self, params: dict) -> dict:
        try:
            res = dict(zip(map(str.encode, params.keys()), self._process_params(params.values())))
        except Exception as err:
            raise ProgrammingError(f"Failed processing pyformat-parameters; {err}")
        else:
            return res

    def _process_params(self, params: Sequence) -> tuple:
        res = []
        for p in params:
            if isinstance(p, bool):
                res.append(f"{p}".lower())
            elif isinstance(p, str):
                res.append(f"'{p}'")
            elif not isinstance(p, str):
                res.append(f"{p}")
            else:
                res.append(p)
        return tuple(map(str.encode, res))
