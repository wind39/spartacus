import Spartacus
from Spartacus import Database

try:
    v_source = Spartacus.Database.SQLite('samples/employees.db')
    v_target = Spartacus.Database.SQLite('samples/employees.db')

    #v_source = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')
    #v_target = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_source.Open()
    v_target.Open()

    v_target.Execute('create table departments2 (id text, name text)')

    v_fields = [Spartacus.Database.DataField('id'), Spartacus.Database.DataField('name')]

    b = 1
    v_hasmorerecords = True
    while v_hasmorerecords:
        v_table = v_source.QueryBlock('select * from departments', 4)

        if len(v_table.Rows) > 0:
            print("Block {0}: {1} record(s)".format(b, len(v_table.Rows)))
            print(v_table.Pretty())
            print('')

            v_target.InsertBlock(v_table, 'departments2', v_fields)

            print('{0} rows inserted'.format(len(v_table.Rows)))
            print('')

            b = b + 1
        else:
            v_hasmorerecords = False

    v_target.Execute('drop table departments2')

    v_source.Close()
    v_target.Close()
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
