import Spartacus
import Spartacus.Database

try:
    #v_database = Spartacus.Database.SQLite('employees.db')
    v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_result = v_database.ExecuteScalar("select dept_name from departments where dept_no = 'd005'")

    print(v_result)
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
