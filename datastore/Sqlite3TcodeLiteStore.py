import sqlite3
import logging


# sqlite3:
#   https://docs.python.org/3/library/sqlite3.html
# sqlite3 tool:
#   https://sqlitestudio.pl/index.rvt?act=download

class Sqlite3TcodeLiteStore:

    def __init__(self, db):

        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS tcode (TCODE text PRIMARY KEY, TCODE_DESC text, comments text, favorite text)')
        self.conn.commit()
        logging.info(f'Initial Sqlite3TcodeLiteStore -> {db}')

    def fetchAllTcode(self, limit=1000):
        self.cursor.execute(
            'SELECT TCODE, TCODE_DESC, comments, favorite FROM tcode order by favorite, TCODE asc LIMIT ?',
            (limit,))
        rows = self.cursor.fetchall()
        logging.info(f'Fetch top {len(rows)} records.')
        return rows

    def insertOrUpdateTcode(self, TCODE, TCODE_DESC, comments='', favorite='Z'):
        self.cursor.execute("select tcode from TCODE where tcode=?", (TCODE,))
        found = self.cursor.fetchone()
        if found:
            # update
            self.cursor.execute('UPDATE tcode SET TCODE_DESC=?, comments=?,  favorite=? WHERE TCODE=?',
                                (TCODE_DESC, comments, favorite, TCODE))
            self.conn.commit()
            logging.info(
                f'update -> {TCODE},{TCODE_DESC},{comments},{favorite}')
        else:
            # new
            self.cursor.execute('INSERT INTO tcode VALUES(?, ?, ?, ?)', (TCODE, TCODE_DESC, comments, favorite))
            self.conn.commit()
            logging.info(f'insert -> {TCODE},{TCODE_DESC},{comments},{favorite}')

    def deleteTcode(self, TCODE):
        if TCODE:
            self.cursor.execute('DELETE FROM tcode where TCODE like ?', (TCODE,))
            self.conn.commit()
            logging.info(f'delete record with TCODE -> {TCODE}')
        else:
            logging.info('please given TCODE before delete.')

    def searchTcode(self, TCODE, TCODE_DESC='', comments='', favorite='', limit='1000'):
        sql = 'SELECT TCODE, TCODE_DESC, comments, favorite FROM tcode where 1=1  '
        orderby = ' order by favorite, TCODE asc LIMIT ' + limit

        # sql += self._appendLikeQuery(sql, 'TCODE', TCODE)
        sql += self._appendStartwithQuery(sql, 'TCODE', TCODE)
        sql += self._appendLikeQuery(sql, 'TCODE_DESC', TCODE_DESC)
        sql += self._appendLikeQuery(sql, 'comments', comments)
        sql += self._appendLikeQuery(sql, 'favorite', favorite)

        sql += orderby

        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        logging.info(f'Found {len(rows)} records via sql:  -  {sql}')
        return rows

    def _appendLikeQuery(self, sql, field, valueLike):
        if valueLike:
            return " and " + field + " like '%" + \
                self._removebadchar(valueLike) + "%'"

        return ''

    def _appendStartwithQuery(self, sql, field, valueLike):
        if valueLike:
            return " and " + field + " like '" + \
                self._removebadchar(valueLike) + "%'"

        return ''

    def _removebadchar(self, value):
        return self.removechar(value, '=:*?"\'<>|-')

    def removechar(self, value, deletechars):
        for c in deletechars:
            value = value.replace(c, '')
        return value

    def __del__(self):
        self.conn.close()
