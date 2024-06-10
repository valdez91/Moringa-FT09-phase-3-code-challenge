from models import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if id:
            self._id = id
            self._name = self._fetch_name_by_id(id)
        elif name:
            self._name = name
            self._id = self._insert_author(name)

    def _insert_author(self, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return author_id

    def _fetch_name_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM authors WHERE id = ?', (id,))
        author = cursor.fetchone()
        conn.close()
        if author:
            return author['name']
        return None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        from models.article import Article  # Local import to avoid circular dependency
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(**article) for article in articles]

    def magazines(self):
        from models.magazine import Magazine  # Local import to avoid circular dependency
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(**magazine) for magazine in magazines]

    def __repr__(self):
        return f'<Author {self.name}>'
