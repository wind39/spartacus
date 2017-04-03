import Spartacus
from Spartacus import Database

try:
    v_database = Spartacus.Database.SQLite('../employees.db')
    #v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_database.Open()

    b = 1
    v_hasmorerecords = True
    while v_hasmorerecords:
        v_table = v_database.QueryBlock('select * from departments', 4)
        #v_table = v_database.QueryBlock('select * from salaries', 4)

        if len(v_table.Rows) > 0:
            print("Block {0}: {1} record(s)".format(b, len(v_table.Rows)))

            for c in v_table.Columns:
                print('{0}|'.format(c), end='')
            print('')
            for r in v_table.Rows:
                for c in v_table.Columns:
                    print('{0}|'.format(r[c]), end='')
                print('')
            print('')

            b = b + 1
            v_hasmorerecords = True
        else:
            v_hasmorerecords = False

    v_database.Close()
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
