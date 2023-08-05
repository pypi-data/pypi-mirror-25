import unittest
import sqlite3
from breezeblocks import Database, Table
from breezeblocks.sql.join import InnerJoin
from breezeblocks.sql.operators import Equal_, In_
from breezeblocks.sql.values import QmarkStyleValue as Value

import os
DB_URL = os.path.join(os.path.dirname(__file__), 'Chinook.sqlite')

class SQLiteChinookTests(unittest.TestCase):
    """Tests using SQLite with the Chinook Database"""
    
    def setUp(self):
        """Performs necessary SQLite3 setup."""
        self.db = Database(DB_URL, sqlite3)
        self.tables = {
            'Artist': Table('Artist', ['ArtistId', 'Name']),
            'Genre': Table('Genre', ['GenreId', 'Name']),
            'Album': Table('Album', ['AlbumId', 'Title', 'ArtistId']),
            'Track': Table('Track',
                ['TrackId', 'Name', 'AlbumId', 'MediaTypeId', 'GenreId', 'Composer', 'Milliseconds', 'Bytes', 'UnitPrice'])
        }
    
    def test_innerJoin(self):
        tbl_genre = self.tables['Genre']
        tbl_track = self.tables['Track']
    
        tbl_joinGenreTrack = InnerJoin(tbl_track, tbl_genre, using=['GenreId'])
    
        q = self.db.query(
            tbl_joinGenreTrack.left.getColumn('Name'),
            tbl_joinGenreTrack.right.getColumn('Name'))\
            .from_(tbl_joinGenreTrack)\
            .where(Equal_(tbl_joinGenreTrack.right.getColumn('Name'), Value('Classical')))
    
        for row in q.execute():
            self.assertEqual(2, len(row))
