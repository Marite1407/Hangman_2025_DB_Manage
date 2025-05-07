import sqlite3
import os

class Database:
    def __init__(self, db_name='hangman_2025.db'):
        """
        Loob ühenduse andmebaasiga ja kontrollib, kas vajalik tabel on olemas.
        """
        
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)

        print(f"DEBUG: Avan andmebaasi {self.db_path}")  # Kontrollime, kus see fail asub!

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()


    def create_table(self):
        """
        Kontrollib, kas tabel "words" on olemas, kui ei ole, siis loob selle.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_word(self, word, category):
        """
        Lisab uue sõna ja kategooria andmebaasi.
        """
        self.cursor.execute('INSERT INTO words (word, category) VALUES (?, ?)', (word, category))
        self.connection.commit()

        # Kontrollime, kas sõna lisati edukalt
        self.cursor.execute('SELECT * FROM words')
        print("DEBUG: Andmebaasi sisu pärast lisamist:", self.cursor.fetchall())

    def update_word(self, word_id, new_word, new_category):
        """
        Uuendab olemasolevat sõna ja kategooriat.
        """
        self.cursor.execute('UPDATE words SET word = ?, category = ? WHERE id = ?', (new_word, new_category, word_id))
        self.connection.commit()

    def delete_word(self, word_id):
        """
        Kustutab sõna andmebaasist ID alusel.
        """
        self.cursor.execute('DELETE FROM words WHERE id = ?', (word_id,))
        self.connection.commit()

    def get_all_words(self):
        """
        Tagastab kõik sõnad ja nende kategooriad.
        """
        self.cursor.execute('SELECT * FROM words')
        return self.cursor.fetchall()

    def close_connection(self):
        """
        Sulgeb andmebaasi ühenduse.
        """
        self.connection.close()

    def word_exists(self, word, category):
        """
        Kontrollib, kas antud sõna ja kategooria kombinatsioon on juba andmebaasis.
        """
        self.cursor.execute("SELECT id FROM words WHERE word = ? AND category = ?", (word, category))
        return self.cursor.fetchone() is not None

    def get_all_categories(self):
        """
        Tagastab kõik unikaalsed kategooriad andmebaasist.
        """
        self.cursor.execute("SELECT DISTINCT category FROM words")
        categories = [row[0] for row in self.cursor.fetchall()]

        print(f"DEBUG: get_all_categories() tulemused: {categories}")  # Kontrollime, kas "Värvid" on andmebaasis

        return categories


# Testimine
if __name__ == "__main__":
    db = Database()
    db.add_word("Auto", "Sõidukid")
    db.add_word("Koer", "Loomad")
    print(db.get_all_words())
    db.update_word(1, "Buss", "Sõidukid")
    print(db.get_all_words())
    db.delete_word(2)
    print(db.get_all_words())
    db.close_connection()

