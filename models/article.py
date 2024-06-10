from models import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author=None, magazine=None):
        if id:
            self._id = id
            self._title, self._content, self._author_id, self._magazine_id = self._fetch_details_by_id(id)
        elif title and content and author and magazine:
            self._title = title
            self._content = content
            self._author_id = author.id
            self._magazine_id = magazine.id
            self._id = self._insert_article(title, content, author.id, magazine.id)

    def _insert_article(self, title, content, author_id, magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id) 
            VALUES (?, ?, ?, ?)
        ''', (title, content, author_id, magazine_id))
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return article_id

    def _fetch_details_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title, content, author_id, magazine_id FROM articles WHERE id = ?', (id,))
        article = cursor.fetchone()
        conn.close()
        if article:
            return article['title'], article['content'], article['author_id'], article['magazine_id']
        return None, None, None, None

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        from models.author import Author  # Local import to avoid circular dependency
        return Author(id=self._author_id)

    @property
    def magazine(self):
        from models.magazine import Magazine  # Local import to avoid circular dependency
        return Magazine(id=self._magazine_id)

    def __repr__(self):
        return f'<Article {self.title}>'
