import unittest
import sqlite3
from breezeblocks import Database, Table
from breezeblocks.sql.operators import In_
from breezeblocks.sql.values import QmarkStyleValue as Value

import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'Library.sqlite')

class SQLiteLibraryTests(unittest.TestCase):
    """Tests using SQLite on the Library Database."""
    
    def setUp(self):
        """Performs necessary SQLite3 setup"""
        self.db = Database(DB_PATH, sqlite3)
        self.tables = {
            'Book': Table('Book', ['Id', 'Title', 'GenreId']),
            'Genre': Table('Genre', ['Id', 'Name']),
            'Author': Table('Author', ['Id', 'Name']),
            'BookAuthor': Table('BookAuthor', ['BookId', 'AuthorId'])
        }
    
    def test_tableQuery(self):
        q = self.db.query(self.tables['Author'])
    
        for row in q.execute():
            self.assertTrue(hasattr(row, 'Id'))
            self.assertTrue(hasattr(row, 'Name'))
    
    def test_columnQuery(self):
        q = self.db.query(self.tables['Book'].getColumn('Title'))
    
        for row in q.execute():
            self.assertTrue(hasattr(row, 'Title'))
            self.assertFalse(hasattr(row, 'GenreId'))
