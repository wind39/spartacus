import Spartacus
from Spartacus import Database

try:
    v_database = Spartacus.Database.SQLite('samples/employees.db')
    #v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_table = v_database.Query('select * from departments')
    #v_table = v_database.Query("select 1 as id, 'William' as name, cast('1988-05-08' as timestamp) as birth_date, 9.8 as grade")

    v_fields = []
    for c in v_table.Columns:
        print('{0}|'.format(c), end='')
        v_fields.append(Spartacus.Database.DataField(c))
    print('')

    for r in v_table.Rows:
        for c in v_table.Columns:
            print('{0}|'.format(r[c]), end='')
        print(v_database.Mogrify(r, v_fields))
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
