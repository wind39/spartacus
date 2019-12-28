import unittest
import datetime
import decimal
import Spartacus.Database


class TestPostgreSQL12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v_database = Spartacus.Database.PostgreSQL(
            "127.0.0.1", 5412, "spartacus", "spartacus", "spartacus"
        )
        cls.v_database.Open()
        cls.v_database.Execute(
            """
            DROP TABLE IF EXISTS departments;
            DROP TABLE IF EXISTS employees;
        """
        )
        cls.v_database.Execute(
            """
            CREATE TABLE departments (
                dept_no char(4) not null,
                dept_name varchar(40) not null
            );
        """
        )
        cls.v_database.Execute(
            """
            INSERT INTO departments VALUES('d009','Customer Service');
            INSERT INTO departments VALUES('d005','Development');
            INSERT INTO departments VALUES('d002','Finance');
            INSERT INTO departments VALUES('d003','Human Resources');
            INSERT INTO departments VALUES('d001','Marketing');
            INSERT INTO departments VALUES('d004','Production');
            INSERT INTO departments VALUES('d006','Quality Management');
            INSERT INTO departments VALUES('d008','Research');
            INSERT INTO departments VALUES('d007','Sales');
        """
        )
        cls.v_database.Execute(
            """
            CREATE TABLE employees (
                emp_no integer not null,
                birth_date text not null,
                first_name varchar(14) not null,
                last_name varchar(16) not null,
                gender varchar(500) not null,
                hire_date text not null
            );
        """
        )
        cls.v_database.Close()

    @classmethod
    def tearDownClass(cls):
        cls.v_database.Open()
        cls.v_database.Execute(
            """
            DROP TABLE IF EXISTS departments;
            DROP TABLE IF EXISTS employees;
        """
        )
        cls.v_database.Close()

    def test_open_close(self):
        self.assertIsInstance(self.v_database, Spartacus.Database.PostgreSQL)
        self.v_database.Open()
        self.assertIsNot(self.v_database.v_con, None)
        self.v_database.Close()
        self.assertIs(self.v_database.v_con, None)

    def test_getconstatus(self):
        self.assertEqual(self.v_database.GetConStatus(), 0)
        self.v_database.Open()
        self.assertEqual(self.v_database.GetConStatus(), 1)
        self.v_database.Close()
        self.assertEqual(self.v_database.GetConStatus(), 0)

    def test_open_autocommit_enabled(self):
        self.v_database.Open(p_autocommit=True)
        self.assertIsNot(self.v_database.v_con, None)
        self.assertTrue(self.v_database.v_con.autocommit)
        self.v_database.Close()

    def test_open_autocommit_disabled(self):
        self.v_database.Open(p_autocommit=False)
        self.assertIsNot(self.v_database.v_con, None)
        self.assertFalse(self.v_database.v_con.autocommit)
        self.v_database.Close()

    def test_executescalar(self):
        v_result = self.v_database.ExecuteScalar(
            "select dept_name from departments where dept_no = 'd005'"
        )
        self.assertEqual(v_result, "Development")

    def test_execute(self):
        self.v_database.Open()
        self.v_database.Execute(
            "insert into departments (dept_no, dept_name) values ('d000', 'Spartacus')"
        )
        v_result = self.v_database.ExecuteScalar(
            "select dept_name from departments where dept_no = 'd000'"
        )
        self.v_database.Execute("delete from departments where dept_no = 'd000'")
        self.v_database.Close()
        self.assertEqual(v_result, "Spartacus")

    def test_commit(self):
        self.v_database.Open(p_autocommit=False)
        self.v_database.Execute(
            "insert into departments (dept_no, dept_name) values ('d000', 'Spartacus')"
        )
        self.v_database.Commit()
        self.v_database.Close()
        self.v_database.Open()
        v_result = self.v_database.ExecuteScalar(
            "select dept_name from departments where dept_no = 'd000'"
        )
        self.v_database.Execute("delete from departments where dept_no = 'd000'")
        self.v_database.Close()
        self.assertEqual(v_result, "Spartacus")

    def test_rollback(self):
        self.v_database.Open(p_autocommit=False)
        self.v_database.Execute(
            "insert into departments (dept_no, dept_name) values ('d000', 'Spartacus')"
        )
        self.v_database.Rollback()
        self.v_database.Close()
        v_result = self.v_database.ExecuteScalar(
            "select dept_name from departments where dept_no = 'd000'"
        )
        self.assertIs(v_result, None)

    def test_close_commit(self):
        self.v_database.Open(p_autocommit=False)
        self.v_database.Execute(
            "insert into departments (dept_no, dept_name) values ('d000', 'Spartacus')"
        )
        self.v_database.Close(p_commit=True)
        self.v_database.Open()
        v_result = self.v_database.ExecuteScalar(
            "select dept_name from departments where dept_no = 'd000'"
        )
        self.v_database.Execute("delete from departments where dept_no = 'd000'")
        self.v_database.Close()
        self.assertEqual(v_result, "Spartacus")

    def test_close_rollback(self):
        self.v_database.Open(p_autocommit=False)
        self.v_database.Execute(
            "insert into departments (dept_no, dept_name) values ('d000', 'Spartacus')"
        )
        self.v_database.Close(p_commit=False)
        v_result = self.v_database.ExecuteScalar(
            "select dept_name from departments where dept_no = 'd000'"
        )
        self.assertIs(v_result, None)

    def test_getfields(self):
        v_result = self.v_database.GetFields(
            """
            SELECT 1 AS id,
                   'Spartacus'::text AS name,
                   '1988-05-08 17:00:00'::timestamp without time zone AS birth_date,
                   9.8 AS grade
        """
        )
        self.assertEqual(len(v_result), 4)
        for r in v_result:
            self.assertIsInstance(r, Spartacus.Database.DataField)
        self.assertEqual(v_result[0].v_name, "id")
        self.assertIs(v_result[0].v_type, int)
        self.assertEqual(v_result[0].v_dbtype, "int4")
        self.assertEqual(v_result[1].v_name, "name")
        self.assertIs(v_result[1].v_type, str)
        self.assertEqual(v_result[1].v_dbtype, "text")
        self.assertEqual(v_result[2].v_name, "birth_date")
        self.assertIs(v_result[2].v_type, datetime.datetime)
        self.assertEqual(v_result[2].v_dbtype, "timestamp")
        self.assertEqual(v_result[3].v_name, "grade")
        self.assertIs(v_result[3].v_type, decimal.Decimal)
        self.assertEqual(v_result[3].v_dbtype, "numeric")

    def test_query(self):
        v_result = self.v_database.Query("select * from departments order by dept_no")
        self.assertIsInstance(v_result, Spartacus.Database.DataTable)
        v_template = ["dept_no", "dept_name"]
        self.assertListEqual(v_result.Columns, v_template)
        self.assertEqual(len(v_result.Rows), 9)
        self.assertEqual(v_result.Rows[0]["dept_no"], "d001")
        self.assertEqual(v_result.Rows[0]["dept_name"], "Marketing")
        self.assertEqual(v_result.Rows[1]["dept_no"], "d002")
        self.assertEqual(v_result.Rows[1]["dept_name"], "Finance")
        self.assertEqual(v_result.Rows[2]["dept_no"], "d003")
        self.assertEqual(v_result.Rows[2]["dept_name"], "Human Resources")
        self.assertEqual(v_result.Rows[3]["dept_no"], "d004")
        self.assertEqual(v_result.Rows[3]["dept_name"], "Production")
        self.assertEqual(v_result.Rows[4]["dept_no"], "d005")
        self.assertEqual(v_result.Rows[4]["dept_name"], "Development")
        self.assertEqual(v_result.Rows[5]["dept_no"], "d006")
        self.assertEqual(v_result.Rows[5]["dept_name"], "Quality Management")
        self.assertEqual(v_result.Rows[6]["dept_no"], "d007")
        self.assertEqual(v_result.Rows[6]["dept_name"], "Sales")
        self.assertEqual(v_result.Rows[7]["dept_no"], "d008")
        self.assertEqual(v_result.Rows[7]["dept_name"], "Research")
        self.assertEqual(v_result.Rows[8]["dept_no"], "d009")
        self.assertEqual(v_result.Rows[8]["dept_name"], "Customer Service")

    def test_query_simple(self):
        v_result = self.v_database.Query(
            "select * from departments order by dept_no", p_simple=True
        )
        self.assertIsInstance(v_result, Spartacus.Database.DataTable)
        v_template = ["dept_no", "dept_name"]
        self.assertListEqual(v_result.Columns, v_template)
        self.assertEqual(len(v_result.Rows), 9)
        self.assertEqual(v_result.Rows[0][0], "d001")
        self.assertEqual(v_result.Rows[0][1], "Marketing")
        self.assertEqual(v_result.Rows[1][0], "d002")
        self.assertEqual(v_result.Rows[1][1], "Finance")
        self.assertEqual(v_result.Rows[2][0], "d003")
        self.assertEqual(v_result.Rows[2][1], "Human Resources")
        self.assertEqual(v_result.Rows[3][0], "d004")
        self.assertEqual(v_result.Rows[3][1], "Production")
        self.assertEqual(v_result.Rows[4][0], "d005")
        self.assertEqual(v_result.Rows[4][1], "Development")
        self.assertEqual(v_result.Rows[5][0], "d006")
        self.assertEqual(v_result.Rows[5][1], "Quality Management")
        self.assertEqual(v_result.Rows[6][0], "d007")
        self.assertEqual(v_result.Rows[6][1], "Sales")
        self.assertEqual(v_result.Rows[7][0], "d008")
        self.assertEqual(v_result.Rows[7][1], "Research")
        self.assertEqual(v_result.Rows[8][0], "d009")
        self.assertEqual(v_result.Rows[8][1], "Customer Service")

    def test_query_types(self):
        v_result = self.v_database.Query(
            """
            SELECT 1 AS id,
                   'Spartacus'::text AS name,
                   '1988-05-08 17:00:00'::timestamp without time zone AS birth_date,
                   9.8 AS grade
        """
        )
        self.assertIsInstance(v_result, Spartacus.Database.DataTable)
        v_template = ["id", "name", "birth_date", "grade"]
        self.assertListEqual(v_result.Columns, v_template)
        self.assertEqual(len(v_result.Rows), 1)
        self.assertEqual(v_result.Rows[0]["id"], 1)
        self.assertIsInstance(v_result.Rows[0]["id"], int)
        self.assertEqual(v_result.Rows[0]["name"], "Spartacus")
        self.assertIsInstance(v_result.Rows[0]["name"], str)
        self.assertEqual(
            v_result.Rows[0]["birth_date"],
            datetime.datetime.strptime("1988-05-08 17:00:00", "%Y-%m-%d %H:%M:%S"),
        )
        self.assertIsInstance(v_result.Rows[0]["birth_date"], datetime.datetime)
        self.assertEqual(float(v_result.Rows[0]["grade"]), 9.8)
        self.assertIsInstance(v_result.Rows[0]["grade"], decimal.Decimal)

    def test_query_alltypesstr(self):
        v_result = self.v_database.Query(
            """
            SELECT 1 AS id,
                   'Spartacus'::text AS name,
                   '1988-05-08 17:00:00'::timestamp without time zone AS birth_date,
                   9.8 AS grade
            """,
            p_alltypesstr=True,
        )
        self.assertIsInstance(v_result, Spartacus.Database.DataTable)
        v_template = ["id", "name", "birth_date", "grade"]
        self.assertListEqual(v_result.Columns, v_template)
        self.assertEqual(len(v_result.Rows), 1)
        self.assertEqual(v_result.Rows[0]["id"], "1")
        self.assertIsInstance(v_result.Rows[0]["id"], str)
        self.assertEqual(v_result.Rows[0]["name"], "Spartacus")
        self.assertIsInstance(v_result.Rows[0]["name"], str)
        self.assertEqual(v_result.Rows[0]["birth_date"], "1988-05-08 17:00:00")
        self.assertIsInstance(v_result.Rows[0]["birth_date"], str)
        self.assertEqual(v_result.Rows[0]["grade"], "9.8")
        self.assertIsInstance(v_result.Rows[0]["grade"], str)

    def test_queryblock_connection_not_open(self):
        with self.assertRaises(Spartacus.Database.Exception):
            v_result = self.v_database.QueryBlock(
                "select * from departments order by dept_no", 4
            )

    def test_queryblock(self):
        self.v_database.Open()
        self.assertTrue(self.v_database.v_start)
        v_result = self.v_database.QueryBlock(
            "select * from departments order by dept_no", 4
        )
        self.assertFalse(self.v_database.v_start)
        self.assertEqual(len(v_result.Rows), 4)
        v_result = self.v_database.QueryBlock(
            "select * from departments order by dept_no", 4
        )
        self.assertFalse(self.v_database.v_start)
        self.assertEqual(len(v_result.Rows), 4)
        v_result = self.v_database.QueryBlock(
            "select * from departments order by dept_no", 4
        )
        self.assertTrue(self.v_database.v_start)
        self.assertEqual(len(v_result.Rows), 1)
        self.v_database.Close()
        self.assertTrue(self.v_database.v_start)

    def test_insertblock(self):
        v_table = Spartacus.Database.DataTable()
        v_table.AddColumn("dept_no")
        v_table.AddColumn("dept_name")
        v_table.AddRow(["d010", "Spartacus"])
        v_table.AddRow(["d011", "Python"])
        self.v_database.InsertBlock(v_table, "departments")
        v_result = self.v_database.Query(
            "select * from departments where dept_no in ('d010', 'd011')"
        )
        self.assertEqual(len(v_result.Rows), 2)
        self.assertEqual(v_result.Rows[0]["dept_no"], "d010")
        self.assertEqual(v_result.Rows[0]["dept_name"], "Spartacus")
        self.assertEqual(v_result.Rows[1]["dept_no"], "d011")
        self.assertEqual(v_result.Rows[1]["dept_name"], "Python")
        self.v_database.Execute(
            "delete from departments where dept_no in ('d010', 'd011')"
        )

    def test_insertblock_fields(self):
        v_fields = self.v_database.GetFields("select * from employees limit 1")
        v_table = Spartacus.Database.DataTable()
        for f in v_fields:
            v_table.AddColumn(f.v_name)
        v_table.AddRow([500000, "1988-05-08", "Spartacus", "Python", "M", "2006-01-01"])
        v_table.AddRow([500001, "1988-05-08", "Spartacus", "Python", "M", "2006-01-01"])
        self.v_database.InsertBlock(v_table, "employees", v_fields)
        v_result = self.v_database.Query(
            "select * from employees where emp_no in (500000, 500001)"
        )
        self.assertEqual(len(v_result.Rows), 2)
        self.assertEqual(v_result.Rows[0]["emp_no"], 500000)
        self.assertEqual(v_result.Rows[0]["first_name"], "Spartacus")
        self.assertEqual(v_result.Rows[1]["emp_no"], 500001)
        self.assertEqual(v_result.Rows[1]["first_name"], "Spartacus")
        self.v_database.Execute(
            "delete from employees where emp_no in (500000, 500001)"
        )


if __name__ == "__main__":
    unittest.main()
