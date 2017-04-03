import Spartacus
from Spartacus import Database

try:
    v_database = Spartacus.Database.SQLite('../employees.db')
    #v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    #v_table = v_database.Query('select * from departments')
    v_table = v_database.Query('select * from salaries')

    for c in v_table.Columns:
        print('{0}|'.format(c), end='')
    print('')

    for r in v_table.Rows:
        for c in v_table.Columns:
            print('{0}|'.format(r[c]), end='')
        print('')

    #for j in range(0, len(v_table.Columns)):
    #    print('{0}|'.format(v_table.Columns[j]), end='')
    #print('')

    #for i in range(0, len(v_table.Rows)):
    #    for j in range(0, len(v_table.Columns)):
    #        print('{0}|'.format(v_table.Rows[i][j]), end='')
    #    print('')

    #for j in range(0, len(v_table.Columns)):
    #    print('{0}|'.format(v_table.Columns[j]), end='')
    #print('')

    #for i in range(0, len(v_table.Rows)):
    #    print('{0}|'.format(v_table.Rows[i]['emp_no']), end='')
    #    print('{0}|'.format(v_table.Rows[i]['salary']), end='')
    #    print('{0}|'.format(v_table.Rows[i]['from_date']), end='')
    #    print('{0}|'.format(v_table.Rows[i]['to_date']), end='')
    #    print('')
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
