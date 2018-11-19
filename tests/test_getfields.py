import Spartacus
from Spartacus import Database

try:
    v_database = Spartacus.Database.SQLite('samples/employees.db')
    #v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_fields = v_database.GetFields("select * from departments")
    #v_fields = v_database.GetFields("select * from salaries")
    #v_fields = v_database.GetFields("select 1 as id, 'William' as name, cast('1988-05-08' as timestamp) as birth_date, 9.8 as grade")

    for f in v_fields:
        print('{0} {1} {2}'.format(f.v_name, f.v_type, f.v_dbtype))
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
