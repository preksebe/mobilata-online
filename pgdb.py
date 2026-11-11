"""Strat subtire peste PostgreSQL (Supabase), cu aceeasi interfata ca sqlite3 folosita in server.py:
db.execute(sql, params), rânduri accesibile după nume și după index, cursor.lastrowid, commit().
Diferențele față de SQLite sunt tratate aici, ca restul codului să rămână aproape neschimbat.
"""
import datetime
import decimal
import os

import psycopg

IntegrityError = psycopg.IntegrityError


class Row(dict):
    """Rând de rezultat: row["nume"], row[0] și dict(row), ca sqlite3.Row."""

    def __init__(self, keys, values):
        super().__init__(zip(keys, values))
        self._values = list(values)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        return super().__getitem__(key)


def _convert(value):
    # Datele se afișează ca în varianta SQLite: "2026-11-11 14:30".
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, decimal.Decimal):
        return float(value)
    return value


def _row_factory(cursor):
    columns = [d.name for d in cursor.description] if cursor.description else []

    def make(values):
        return Row(columns, [_convert(v) for v in values])

    return make


class Result:
    def __init__(self, cursor, lastrowid=None):
        self._cursor = cursor
        self.lastrowid = lastrowid
        self.rowcount = cursor.rowcount

    def fetchone(self):
        return self._cursor.fetchone() if self._cursor.description else None

    def fetchall(self):
        return self._cursor.fetchall() if self._cursor.description else []

    def __iter__(self):
        return iter(self.fetchall())


class Db:
    def __init__(self, url=None):
        url = url or os.environ.get("DATABASE_URL")
        if not url:
            raise RuntimeError("Lipseste DATABASE_URL (adresa bazei de date Supabase).")
        # prepare_threshold=None: poolerul Supabase in mod "transaction" nu accepta instructiuni pregatite.
        self.conn = psycopg.connect(url, row_factory=_row_factory, prepare_threshold=None, connect_timeout=10)

    def execute(self, sql, params=()):
        sql = sql.replace("%", "%%").replace("?", "%s")
        is_insert = sql.lstrip()[:6].upper() == "INSERT" and "RETURNING" not in sql.upper()
        if is_insert:
            sql += " RETURNING id"
        cur = self.conn.execute(sql, tuple(params))
        lastrowid = None
        if is_insert:
            row = cur.fetchone()
            lastrowid = row["id"] if row else None
        return Result(cur, lastrowid)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.close()
