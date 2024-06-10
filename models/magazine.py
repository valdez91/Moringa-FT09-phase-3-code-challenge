from models import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        if id:
            self._id = id
            self._name, self._category = self._fetch_details_by_id(id)
        elif name and category:
            self._name = name
            self._category = category
            self._id = self._insert_magazine(name, category)

    def _insert_magazine(self, name, category):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return magazine_id

    def _fetch_details_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, category FROM magazines WHERE id = ?', (id,))
        magazine = cursor.fetchone()
        conn.close()
        if magazine:
            return magazine['name'], magazine['category']
        return None, None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if 2 <= len(new_name) <= 16:
            self._name = new_name
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET name = ? WHERE id = ?', (new_name, self.id))
            conn.commit()
            conn.close()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if len(new_category) > 0:
            self._category = new_category
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE magazines SET category = ? WHERE id = ?', (new_category, self.id))
            conn.commit()
            conn.close()

    def articles(self):
        from models.article import Article  # Local import to avoid circular dependency
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(**article) for article in articles]

    def contributors(self):
        from models.author import Author  # Local import to avoid circular dependency
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(**author) for author in authors]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title['title'] for title in titles]

    def contributing_authors(self):
        from models.author import Author  # Local import to avoid circular dependency
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.*, COUNT(articles.id) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(**author) for author in authors]

    def __repr__(self):
        return f'<Magazine {self.name}>'
