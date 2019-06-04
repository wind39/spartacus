import Spartacus
from Spartacus import Database

try:
    v_database = Spartacus.Database.SQLite("samples/employees.db")
    # v_database = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_database.Execute(
        "create table depts1 as select t.*, random() as val from departments t"
    )

    v_database.Execute("create table depts2 as select * from depts1")
    v_database.Execute("delete from depts2 where dept_no in ('d006', 'd009')")
    v_database.Execute("update depts2 set val = 20000 where dept_no = 'd002'")
    v_database.Execute(
        "update depts2 set val = 20020, dept_name = 'Marketing and Promotion' where dept_no = 'd001'"
    )
    v_database.Execute("insert into depts2 values ('d100', 'Test Department1', 1000)")
    v_database.Execute("insert into depts2 values ('d101', 'Test Department2', 1010)")
    v_database.Execute("insert into depts2 values ('d102', 'Test Department3', 1020)")

    v_table_a = v_database.Query("select * from depts1")

    print("Table A:")
    print(v_table_a.Pretty())
    print("")

    v_table_b = v_database.Query("select * from depts2")

    print("Table B:")
    print(v_table_b.Pretty())
    print("")

    v_table_c = v_table_a.Compare(v_table_b, ["dept_no"], "status", "diff", True)

    print("Table C:")
    print(v_table_c.Pretty())

    v_database.Execute("drop table depts1")
    v_database.Execute("drop table depts2")

except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
