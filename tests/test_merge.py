import Spartacus
from Spartacus import Database

try:
    v_database = Spartacus.Database.SQLite('samples/employees.db')
    #v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_table_a = v_database.Query("select dept_no, dept_name, 'A' as test from departments")

    print('Table A:')
    print(v_table_a.Pretty())
    print('')

    v_table_b = v_database.Query("select dept_no, dept_name, 'B' as test from departments")

    print('Table B:')
    print(v_table_b.Pretty())
    print('')

    v_table_a.Merge(v_table_b)

    print('Table A merged with table B:')
    print(v_table_a.Pretty())
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
