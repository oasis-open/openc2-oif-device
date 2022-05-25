from pathlib import Path
from peewee import fn
from osquery_orm import OsQueryDatabase


if __name__ == '__main__':
    db = OsQueryDatabase(f'{Path.home()}/.osquery/osqueryd.sock')
    db.connect()
    print(f"DB: {db}")

    r_qry = db.raw_query("SELECT * FROM os_version")
    print(f"\nRaw Query: {r_qry}")

    c_qry = db.tables.macos.OS_Version.select()
    print(f'\nCode Qry: {c_qry}')
    for itm in c_qry:
        print(f'-- {type(itm)} - {itm.dict()}\n')

    tables = db.get_tables()
    print(f"\nTables: {len(tables):,}\n{tables}\n")

    rslt = db.tables.macos.OS_Version.select()
    print(f"\nOS Version: {list(rslt)}\n")

    proc = db.tables.macos.Processes
    rslt = proc.select().where(fn.Lower(fn.Substr(proc.name, 1, 6)) == 'python')
    print(rslt)
    rslt_rows = '\n--> '.join([str(r.dict()) for r in rslt])
    print(f"\nResults:\n--> {rslt_rows}\n")

