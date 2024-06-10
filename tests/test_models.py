import unittest
import sqlite3
from models import get_db_connection, init_db
from models.author import Author
from models.magazine import Magazine
from models.article import Article

class TestModels(unittest.TestCase):

    def setUp(self):
        # Initialize the database and create tables
        init_db()

        # Insert sample data for testing
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', ("John Doe",))
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', ("Tech Monthly", "Technology"))
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       ("New Tech Trends", "Content about trends", 1, 1))
        conn.commit()
        conn.close()

    def tearDown(self):
        # Clean up the database after each test
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS articles')
        cursor.execute('DROP TABLE IF EXISTS authors')
        cursor.execute('DROP TABLE IF EXISTS magazines')
        conn.commit()
        conn.close()

    def test_author_creation(self):
        author = Author(name="Jane Doe")
        self.assertEqual(author.name, "Jane Doe")

    def test_magazine_creation(self):
        magazine = Magazine(name="Science Weekly", category="Science")
        self.assertEqual(magazine.name, "Science Weekly")
        self.assertEqual(magazine.category, "Science")

    def test_article_creation(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Monthly", category="Technology")
        article = Article(title="Test Title", content="Test Content", author=author, magazine=magazine)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.author.name, "John Doe")
        self.assertEqual(article.magazine.name, "Tech Monthly")

if __name__ == "__main__":
    unittest.main()
