'''
The MIT License (MIT)

Copyright (c) 2017 William Ivanski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from abc import ABC, abstractmethod
import datetime

import sqlite3
import psycopg2
from psycopg2 import extras

import Spartacus

class Exception(Exception):
    pass

class DataTable(object):
    def __init__(self):
        self.Columns = []
        self.Rows = []
    def Merge(self, p_datatable):
        if len(self.Columns) > 0 and len(p_datatable.Columns) > 0:
            if self.Columns == p_datatable.Columns:
                for r in p_datatable.Rows:
                    self.Rows.append(r)
            else:
                raise Spartacus.Database.Exception('Can not merge tables with different columns.')
        else:
            raise Spartacus.Database.Exception('Can not merge tables with no columns.')

class DataField(object):
    def __init__(self, p_name, p_type=None, p_dbtype=None, p_mask='#'):
        self.v_name = p_name
        self.v_type = p_type
        self.v_dbtype = p_dbtype
        self.v_mask = p_mask

class DataTransferReturn(object):
    def __init__(self):
        self.v_numrecords = 0
        self.v_log = None

'''
------------------------------------------------------------------------
Generic
------------------------------------------------------------------------
'''
class Generic(ABC):
    @abstractmethod
    def Open(self):
        pass
    @abstractmethod
    def Query(self, p_sql):
        pass
    @abstractmethod
    def Execute(self, p_sql):
        pass
    @abstractmethod
    def ExecuteScalar(self, p_sql):
        pass
    @abstractmethod
    def Close(self):
        pass
    @abstractmethod
    def GetFields(self, p_sql):
        pass
    @abstractmethod
    def QueryBlock(self, p_sql, p_blocksize):
        pass
    @abstractmethod
    def Mogrify(self, p_row):
        pass
    @abstractmethod
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        pass
    @abstractmethod
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None):
        pass
    @classmethod
    def Mogrify(self, p_row, p_fields):
        if len(p_row) == len(p_fields):
            k = 0
            v_mog = []
            while k < len(p_row):
                if type(p_row[k]) == type(None):
                    v_mog.append('null')
                elif type(p_row[k]) == type(str()) or type(p_row[k]) == datetime.datetime:
                    v_mog.append(p_fields[k].v_mask.replace('#', "'{0}'".format(p_row[k])))
                else:
                    v_mog.append(p_fields[k].v_mask.replace('#', "{0}".format(p_row[k])))
                k = k + 1
            return '(' + ','.join(v_mog) + ')'
        else:
            raise Spartacus.Database.Exception('Can not mogrify with different number of parameters.')

'''
------------------------------------------------------------------------
SQLite
------------------------------------------------------------------------
'''
class SQLite(Generic):
    def __init__(self, p_service):
        self.v_host = None
        self.v_port = None
        self.v_service = p_service
        self.v_user = None
        self.v_password = None
        self.v_con = None
        self.v_cur = None
    def Open(self):
        try:
            self.v_con = sqlite3.connect(self.v_service)
            self.v_con.row_factory = sqlite3.Row
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                self.v_con.commit()
                self.Close()
                return v_table
            else:
                self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                self.v_con.commit()
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Execute(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                self.v_con.commit()
                self.Close()
            else:
                self.v_cur.execute(p_sql)
                self.v_con.commit()
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def ExecuteScalar(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                s = r[0]
                self.v_con.commit()
                self.Close()
                return s
            else:
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                s = r[0]
                self.v_con.commit()
                return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Close(self):
        try:
            self.v_cur.close()
            self.v_cur = None
            self.v_con.close()
            self.v_con = None
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetFields(self, p_sql):
        try:
            if self.v_con is None:
                v_fields = []
                self.Open()
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
                self.v_con.commit()
                self.Close()
                return v_fields
            else:
                v_fields = []
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
                self.v_con.commit()
                return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def QueryBlock(self, p_sql, p_blocksize):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchmany(p_blocksize)
                if len(v_table.Rows) == 0:
                    self.v_con.commit()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_insert = 'begin; '
            for r in p_block.Rows:
                v_insert = v_insert + 'insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + self.Mogrify(r, v_fields) + '; '
            v_insert = v_insert + 'commit;'
            self.Execute(v_insert)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return


'''
------------------------------------------------------------------------
Memory
------------------------------------------------------------------------
'''
class Memory(Generic):
    def __init__(self):
        self.v_host = None
        self.v_port = None
        self.v_service = ':memory:'
        self.v_user = None
        self.v_password = None
        self.v_con = None
        self.v_cur = None
    def Open(self):
        try:
            self.v_con = sqlite3.connect(self.v_service)
            self.v_con.row_factory = sqlite3.Row
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                self.v_con.commit()
                self.Close()
                return v_table
            else:
                self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                self.v_con.commit()
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Execute(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                self.v_con.commit()
                self.Close()
            else:
                self.v_cur.execute(p_sql)
                self.v_con.commit()
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def ExecuteScalar(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                s = r[0]
                self.v_con.commit()
                self.Close()
                return s
            else:
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                s = r[0]
                self.v_con.commit()
                return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Close(self):
        try:
            self.v_cur.close()
            self.v_cur = None
            self.v_con.close()
            self.v_con = None
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetFields(self, p_sql):
        try:
            if self.v_con is None:
                v_fields = []
                self.Open()
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
                self.v_con.commit()
                self.Close()
                return v_fields
            else:
                v_fields = []
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
                self.v_con.commit()
                return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def QueryBlock(self, p_sql, p_blocksize):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchmany(p_blocksize)
                if len(v_table.Rows) == 0:
                    self.v_con.commit()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_insert = 'begin; '
            for r in p_block.Rows:
                v_insert = v_insert + 'insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + self.Mogrify(r, v_fields) + '; '
            v_insert = v_insert + 'commit;'
            self.Execute(v_insert)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return

'''
------------------------------------------------------------------------
PostgreSQL
------------------------------------------------------------------------
'''
class PostgreSQL(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password):
        self.v_host = p_host
        self.v_port = p_port
        self.v_service = p_service
        self.v_user = p_user
        self.v_password = p_password
        self.v_con = None
        self.v_cur = None
        # PostgreSQL types
        self.Open()
        self.v_cur.execute('select oid, typname from pg_type')
        self.v_types = dict([(r['oid'], r['typname']) for r in self.v_cur.fetchall()])
        self.v_con.commit()
        self.Close()
    def Open(self):
        try:
            self.v_con = psycopg2.connect(
                'host={0} port={1} dbname={2} user={3} password={4}'.format(
                    self.v_host,
                    self.v_port,
                    self.v_service,
                    self.v_user,
                    self.v_password
                ),
                cursor_factory=psycopg2.extras.DictCursor)
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                self.v_con.commit()
                self.Close()
                return v_table
            else:
                self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                self.v_con.commit()
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Execute(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                self.v_con.commit()
                self.Close()
            else:
                self.v_cur.execute(p_sql)
                self.v_con.commit()
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def ExecuteScalar(self, p_sql):
        try:
            if self.v_con is None:
                self.Open()
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                s = r[0]
                self.v_con.commit()
                self.Close()
                return s
            else:
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                s = r[0]
                self.v_con.commit()
                return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Close(self):
        try:
            self.v_cur.close()
            self.v_cur = None
            self.v_con.close()
            self.v_con = None
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetFields(self, p_sql):
        try:
            if self.v_con is None:
                v_fields = []
                self.Open()
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                k = 0
                for c in self.v_cur.description:
                    v_type = '{0}'.format(self.v_types[c.type_code])
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=v_type))
                    k = k + 1
                self.v_con.commit()
                self.Close()
                return v_fields
            else:
                v_fields = []
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                k = 0
                for c in self.v_cur.description:
                    v_type = '{0}'.format(self.v_types[c.type_code])
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=v_type))
                    k = k + 1
                self.v_con.commit()
                return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def QueryBlock(self, p_sql, p_blocksize):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchmany(p_blocksize)
                if len(v_table.Rows) == 0:
                    self.v_con.commit()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute('insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + ','.join(v_values) + '')
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
