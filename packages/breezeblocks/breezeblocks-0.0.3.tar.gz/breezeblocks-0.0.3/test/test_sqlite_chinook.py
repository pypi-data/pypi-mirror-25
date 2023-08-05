import unittest
import sqlite3
from breezeblocks import Database, Table
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
    
    def test_tableQuery(self):
        """Tests a simple select on a table."""
        q = self.db.query(self.tables['Artist'])
        
        # Assertion checks that all columns in the table are present in
        # each row returned.
        for row in q.execute():
            self.assertTrue(hasattr(row, 'ArtistId'))
            self.assertTrue(hasattr(row, 'Name'))
    
    def test_columnQuery(self):
        """Tests a simple select on a column."""
        q = self.db.query(self.tables['Artist'].getColumn('Name'))
    
        # Assertion checks that only the queried columns are returned.
        for row in q.execute():
            self.assertTrue(hasattr(row, 'Name'))
            self.assertFalse(hasattr(row, 'ArtistId'))
    
    def test_simpleWhereClause(self):
        """Tests a simple where clause."""
        tbl_genre = self.tables['Genre']
        tbl_track = self.tables['Track']
        genre_id = self.db.query(tbl_genre)\
            .where(tbl_genre.getColumn('Name') == Value('Alternative & Punk'))\
            .execute()[0].GenreId
    
        q = self.db.query(tbl_track.getColumn('GenreId'))\
                .where(tbl_track.getColumn('GenreId') == Value(genre_id))
    
        # Assertion checks that the where condition has been applied to
        # the results of the query.
        for track in q.execute():
            self.assertEqual(genre_id, track.GenreId)
    
    def test_nestedQueryInWhereClause(self):
        tbl_album = self.tables['Album']
        tbl_genre = self.tables['Genre']
        tbl_track = self.tables['Track']
    
        genre_id = self.db.query(tbl_genre)\
            .where(tbl_genre.getColumn('Name') == Value('Alternative & Punk'))\
            .execute()[0].GenreId
    
        q = self.db.query(tbl_album.getColumn('Title'))\
                .where(
                    In_(
                        tbl_album.getColumn('AlbumId'),
                        self.db.query(tbl_track.getColumn('AlbumId'))\
                            .where(tbl_track.getColumn('GenreId') == Value(genre_id))
                    )
                )
    
        # No assertion here because subqueries because subqueries in the select
        # clause have not been implemented.
        # However, the query running without error is important to test.
        q.execute()
    
    def test_aliasTable(self):
        tbl_album = self.tables['Album']
        tbl_artist = self.tables['Artist']
        
        artist_id = self.db.query(tbl_artist.getColumn('ArtistId'))\
            .where(Equal_(tbl_artist.getColumn('Name'), Value('Queen')))\
            .execute()[0].ArtistId
        
        musician = tbl_artist.as_('Musician')
        q = self.db.query(musician).where(Equal_(musician.getColumn('ArtistId'), Value(artist_id)))
        
        for row in q.execute():
            self.assertTrue(hasattr(row, 'ArtistId'))
            self.assertTrue(hasattr(row, 'Name'))
            self.assertEqual(artist_id, row.ArtistId)
    
    def test_selectFromQuery(self):
        tbl_album = self.tables['Album']
        tbl_artist = self.tables['Artist']
        
        artist_id = self.db.query(tbl_artist.getColumn('ArtistId'))\
            .where(Equal_(tbl_artist.getColumn('Name'), Value('Queen')))\
            .execute()[0].ArtistId
        
        inner_q = self.db.query(tbl_album.getColumn('ArtistId'), tbl_album.getColumn('Title'))\
            .where(Equal_(tbl_album.getColumn('ArtistId'), Value(artist_id)))
        
        q = self.db.query(inner_q.as_('q'))
        
        for row in q.execute():
            self.assertTrue(hasattr(row, 'ArtistId'))
            self.assertTrue(hasattr(row, 'Title'))
            self.assertEqual(artist_id, row.ArtistId)
