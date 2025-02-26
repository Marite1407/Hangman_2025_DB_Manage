from models.Database import Database  # Importime Database klassi

class Model:
    def __init__(self):
        """Loob ühenduse andmebaasiga."""
        self.db = Database()

    def add_word(self, word, category):
        """Lisab sõna andmebaasi."""
        self.db.add_word(word, category)

    def update_word(self, word_id, new_word, new_category):
        """Uuendab olemasolevat sõna andmebaasis."""
        self.db.update_word(word_id, new_word, new_category)

    def delete_word(self, word_id):
        """Kustutab sõna andmebaasist."""
        self.db.delete_word(word_id)

    def get_all_words(self):
        """Tagastab kõik sõnad ja nende kategooriad andmebaasist."""
        return self.db.get_all_words()

    def close(self):
        """Sulgeb andmebaasi ühenduse."""
        self.db.close_connection()
