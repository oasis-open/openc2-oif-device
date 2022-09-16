import osquery

from types import MethodType
from typing import Union
from osquery.extension_client import Client
from peewee import Database, SQL, ColumnMetadata, ForeignKeyMetadata, IndexMetadata, OnConflict, ProgrammingError, fn, simple_date_time
from .orm.cursor import OSQueryCursor
from .tables import Tables


class OsQueryDatabase(Database):
    tables: Tables

    def __init__(self, database, *args, **kwargs):
        """
        For an installed and running system osqueryd, this is:
           Linux and macOS: /var/osquery/osquery.em
           FreeBSD: /var/run/osquery.em
           Windows: \\.\pipe\osquery.em
        :param database: database location
        :param comp: OS Compatibility
        :param kwargs:
        :return:
        """
        super().__init__(database, *args, **kwargs)
        self._table_functions = []
        self.tables = Tables(self)

    def _connect(self):
        instance = osquery.ExtensionClient(self.database)
        try:
            instance.open()  # This may raise an exception
        except Exception:
            instance.close()
            raise
        # Issue queries and call osquery Thrift APIs.
        conn = instance.extension_client()
        try:
            if self._table_functions:
                for table_function in self._table_functions:
                    table_function.register(conn)
        except Exception as err:
            raise ProgrammingError from err

        def cursor(self, commit=None):  # pylint: disable=W0613
            return type('Cursor', (OSQueryCursor,), {'_connection': conn})(commit)

        conn.cursor = MethodType(cursor, conn)
        return conn

    def get_tables(self, schema=None):
        table = self.tables._cross_platform.OsqueryRegistry
        # pylint: disable=C0121
        rslts = table.select(table.name).where(table.active == True).where(table.internal == False).where(table.registry == 'table')
        return tuple(sorted(r.name for r in rslts))

    def get_indexes(self, table: str, schema=None):
        schema = schema or 'main'
        query = f'SELECT name, sql FROM "{schema}".sqlite_master WHERE tbl_name = ? AND type = ? ORDER BY name'
        cursor = self.execute_sql(query, (table, 'index'))
        index_to_sql = dict(cursor.fetchall())

        # Determine which indexes have a unique constraint.
        unique_indexes = set()
        cursor = self.execute_sql(f'PRAGMA "{schema}".index_list("{table}")')
        for row in cursor.fetchall():
            name = row[1]
            is_unique = int(row[2]) == 1
            if is_unique:
                unique_indexes.add(name)

        # Retrieve the indexed columns.
        index_columns = {}
        for index_name in sorted(index_to_sql):
            cursor = self.execute_sql(f'PRAGMA "{schema}".index_info("{index_name}")')
            index_columns[index_name] = [row[2] for row in cursor.fetchall()]

        return [IndexMetadata(
            name,
            index_to_sql[name],
            index_columns[name],
            name in unique_indexes,
            table
        ) for name in sorted(index_to_sql)]

    def get_columns(self, table: str, schema=None):
        cursor = self.execute_sql(f'PRAGMA "{schema or "main"}".table_info("{table}")')
        return [ColumnMetadata(r[1], r[2], not r[3], bool(r[5]), table, r[4]) for r in cursor.fetchall()]

    def get_primary_keys(self, table: str, schema=None):
        cursor = self.execute_sql(f'PRAGMA "{schema or "main"}".table_info("{table}")')
        return [row[1] for row in filter(lambda r: r[-1], cursor.fetchall())]

    def get_foreign_keys(self, table: str, schema=None):
        cursor = self.execute_sql(f'PRAGMA "{schema or "main"}".foreign_key_list("{table}")')
        return [ForeignKeyMetadata(row[3], row[2], row[4], table) for row in cursor.fetchall()]

    def sequence_exists(self, seq):
        pass

    def conflict_statement(self, on_conflict: OnConflict, query):
        action = on_conflict._action.lower() if on_conflict._action else ''
        if action and action not in ('nothing', 'update'):
            return SQL(f'INSERT OR {on_conflict._action.upper()}')

    def conflict_update(self, on_conflict: OnConflict, query):
        # Sqlite prior to 3.24.0 does not support Postgres-style upsert.
        if self.server_version < (3, 24, 0) and any((on_conflict._preserve, on_conflict._update, on_conflict._where, on_conflict._conflict_target, on_conflict._conflict_constraint)):
            raise ValueError('SQLite does not support specifying which values to preserve or update.')

        action = on_conflict._action.lower() if on_conflict._action else ''
        if action and action not in ('nothing', 'update', ''):
            return

        if action == 'nothing':
            return SQL('ON CONFLICT DO NOTHING')
        if not on_conflict._update and not on_conflict._preserve:
            raise ValueError('If you are not performing any updates (or preserving any INSERTed values), then the conflict resolution action should be set to "NOTHING".')
        if on_conflict._conflict_constraint:
            raise ValueError('SQLite does not support specifying named constraints for conflict resolution.')
        if not on_conflict._conflict_target:
            raise ValueError('SQLite requires that a conflict target be specified when doing an upsert.')
        return self._build_on_conflict_update(on_conflict, query)

    def extract_date(self, date_part, date_field):
        return fn.date_part(date_part, date_field, python_value=int)

    def truncate_date(self, date_part, date_field):
        return fn.date_trunc(date_part, date_field, python_value=simple_date_time)

    def to_timestamp(self, date_field):
        return fn.strftime('%s', date_field).cast('integer')

    def from_timestamp(self, date_field):
        return fn.datetime(date_field, 'unixepoch')

    def _setTableDB(self, conn: Client):
        pass

    # Custom Function
    def raw_query(self, sql: Union[bytes, bytearray, str], params: tuple = ()):
        cur = self.cursor()
        cur.execute(sql, params)
        return cur.fetchall()
