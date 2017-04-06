import Spartacus
from Spartacus import Database

try:
    #v_database = Spartacus.Database.SQLite('../employees.db')
    v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    #v_table = v_database.Query('select * from departments', True)
    v_table = v_database.Query('select * from salaries', True)

    for r in v_table.Rows:
        print(r)
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
