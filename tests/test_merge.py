import Spartacus
from Spartacus import Database

try:
    v_database = Spartacus.Database.SQLite('../employees.db')
    #v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_table_a = v_database.Query("select dept_no, dept_name, 'A' as test from departments")

    print('Table A:')
    for c in v_table_a.Columns:
        print('{0}|'.format(c), end='')
    print('')
    for r in v_table_a.Rows:
        for c in v_table_a.Columns:
            print('{0}|'.format(r[c]), end='')
        print('')
    print('')

    v_table_b = v_database.Query("select dept_no, dept_name, 'B' as test from departments")

    print('Table B:')
    for c in v_table_b.Columns:
        print('{0}|'.format(c), end='')
    print('')
    for r in v_table_b.Rows:
        for c in v_table_b.Columns:
            print('{0}|'.format(r[c]), end='')
        print('')
    print('')

    v_table_a.Merge(v_table_b)

    print('Table A merged with table B:')
    for c in v_table_a.Columns:
        print('{0}|'.format(c), end='')
    print('')
    for r in v_table_a.Rows:
        for c in v_table_a.Columns:
            print('{0}|'.format(r[c]), end='')
        print('')
    print('')
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
