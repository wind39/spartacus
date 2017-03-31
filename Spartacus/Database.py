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

class DataBlock(object):
    def __init__(self):
        self.NumRecords = 0
        self.Log = []
        self.Data = DataTable()

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
    def InsertBlock(self, p_sql, p_rows, p_columnnames=None):
        pass
    @abstractmethod
    def Transfer(self, p_sql, p_insert, p_destdatabase, p_blocksize):
        pass

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
                self.v_cur.fetchall()
                self.v_con.commit()
                self.Close()
                return s
            else:
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                s = r[0]
                self.v_cur.fetchall()
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
        raise Spartacus.Database.Exception ('Not Implemented')
    def QueryBlock(self, p_sql, p_blocksize):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                    self.v_start = False
                v_block = DataBlock()
                for c in self.v_cur.description:
                    v_block.Data.Columns.append(c[0])
                v_hasmorerecords = True
                while v_hasmorerecords and v_block.NumRecords < p_blocksize:
                    r = self.v_cur.fetchone()
                    if r is not None:
                        v_block.Data.Rows.append(r)
                        v_block.NumRecords = v_block.NumRecords + 1
                        v_hasmorerecords = True
                    else:
                        self.v_con.commit()
                        v_hasmorerecords = False
                return v_block
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_sql, p_rows, p_columnnames=None):
        raise Spartacus.Database.Exception ('Not Implemented')
    def Transfer(self, p_query, p_insert, p_destdatabase, p_blocksize):
        raise Spartacus.Database.Exception ('Not Implemented')

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
                    v_table.Columns.append(c.name)
                v_table.Rows = self.v_cur.fetchall()
                self.v_con.commit()
                self.Close()
                return v_table
            else:
                self.v_cur.execute(p_sql)
                v_table = DataTable()
                for c in self.v_cur.description:
                    v_table.Columns.append(c.name)
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
                self.v_cur.fetchall()
                self.v_con.commit()
                self.Close()
                return s
            else:
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                s = r[0]
                self.v_cur.fetchall()
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
        raise Spartacus.Database.Exception ('Not Implemented')
    def QueryBlock(self, p_sql, p_blocksize):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                    self.v_start = False
                v_block = DataBlock()
                for c in self.v_cur.description:
                    v_block.Data.Columns.append(c.name)
                v_hasmorerecords = True
                while v_hasmorerecords and v_block.NumRecords < p_blocksize:
                    r = self.v_cur.fetchone()
                    if r is not None:
                        v_block.Data.Rows.append(r)
                        v_block.NumRecords = v_block.NumRecords + 1
                        v_hasmorerecords = True
                    else:
                        self.v_con.commit()
                        v_hasmorerecords = False
                return v_block
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_sql, p_rows, p_columnnames=None):
        raise Spartacus.Database.Exception ('Not Implemented')
    def Transfer(self, p_query, p_insert, p_destdatabase, p_blocksize):
        raise Spartacus.Database.Exception ('Not Implemented')
