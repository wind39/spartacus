import Spartacus
from Spartacus import Database

try:
    v_source = Spartacus.Database.SQLite('samples/employees.db')
    v_target = Spartacus.Database.PostgreSQL('127.0.0.1', '5432', 'employees', 'william', 'password')

    v_source.Open()
    v_target.Open()

    #v_target.Execute('create table departments2 (id text, name text)')
    #v_fields = [Spartacus.Database.DataField('id'), Spartacus.Database.DataField('name')]

    v_target.Execute('create table salaries2 (emp_no int, salary bigint, from_date timestamp, to_date timestamp)')

    v_hasmorerecords = True
    v_numtotalrecords = 0
    while v_hasmorerecords:
        #v_return = v_source.Transfer('select * from departments', v_target, 'departments2', 4, v_fields)
        v_return = v_source.Transfer('select * from salaries', v_target, 'salaries2', 400)

        if v_return.v_log is not None:
            print('Error: {0}'.format(v_return.v_log))

        if v_return.v_numrecords > 0:
            v_numtotalrecords = v_numtotalrecords + v_return.v_numrecords
            print('Transfered {0} records'.format(v_numtotalrecords))
        else:
            v_hasmorerecords = False

    #v_target.Execute('drop table departments2')
    v_target.Execute('drop table salaries2')

    v_source.Close()
    v_target.Close()
except Spartacus.Database.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
