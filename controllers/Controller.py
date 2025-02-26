import os
from tkinter.filedialog import askopenfilename
from tkinter import END, messagebox
from models.Database import Database  # Kontrolli, et see import oleks olemas!

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Sidume nupud funktsioonidega
        self.view.get_buttons[0].config(command=self.add_word)  # Lisa
        self.view.get_buttons[1].config(command=self.update_word)  # Muuda
        self.view.get_buttons[2].config(command=self.delete_word)  # Kustuta
        self.view.get_buttons[3].config(command=self.open_database)  # Ava nupp

        # Esialgne andmete kuvamine
        self.update_table()

    def open_database(self):
        """
        Avab kasutaja valitud andmebaasi. Kui andmebaas on vigane või puudub tabel words,
        luuakse uus 'hangman_2025.db' koos õige struktuuriga.
        """
        db_path = askopenfilename(title="Vali andmebaas", filetypes=[("SQLite Database", "*.db")], initialdir=os.getcwd())

        if not db_path:  # Kui kasutaja vajutab "Cancel", siis ei tehta midagi
            return

        print(f"DEBUG: Kasutaja valis andmebaasi: {db_path}")

        # Loome uue Database objekti
        self.model.db = Database(db_path)

        # Kontrollime, kas andmebaasis on vajalik tabel ja struktuur
        self.model.db.cursor.execute("PRAGMA table_info(words)")
        columns = self.model.db.cursor.fetchall()

        required_columns = {"id", "word", "category"}  # Õiged veerud
        found_columns = {col[1] for col in columns}  # Andmebaasist leitud veerud

        if "words" not in self.get_existing_tables() or found_columns != required_columns:
            messagebox.showwarning("Viga", "Valitud andmebaasis puudub õige struktuur. Luuakse uus andmebaas!")

            if db_path != os.path.join(os.getcwd(), "hangman_2025.db"):
                messagebox.showinfo("Teavitus", f"Uus andmebaas luuakse projekti juurkausta:\n{os.getcwd()}")

            os.remove(db_path)  # Kustutame vale andmebaasi
            self.model.db = Database(os.path.join(os.getcwd(), "hangman_2025.db"))  # Loome uue

        # Uuendame tabeli vaadet
        self.update_table()

    def get_existing_tables(self):
        """
        Kontrollib, millised tabelid on andmebaasis olemas.
        """
        self.model.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.model.db.cursor.fetchall()
        return {table[0] for table in tables}

    def add_word(self, event=None):  # Lisasime event=None, et see saaks töötada ka ENTER-iga
        """
        Lisab uue sõna andmebaasi ja uuendab tabelit, kui seda pole varem olemas.
        """
        word = self.view.get_txt_word.get().strip()

        # Kontrollime, kas kasutaja valis olemasoleva kategooria või sisestas uue
        if self.view.get_combo_categories.current() > 0:  # Kui valiti olemasolev
            category = self.view.get_combo_categories.get().strip()
        else:  # Kui sisestati uus kategooria käsitsi
            category = self.view.get_txt_category.get().strip()

        print(f"DEBUG: Sisestatud sõna: '{word}', kategooria: '{category}'")  # ✅ Kontrollime sisestatud väärtused

        if word and category and category != "Vali kategooria":
            # Kontrollime, kas sõna on juba andmebaasis
            if self.model.db.word_exists(word, category):
                messagebox.showwarning("Hoiatus", "See sõna on juba andmebaasis olemas!")
                return

            self.model.add_word(word, category)
            self.update_table()

            self.update_category_combobox()  # ✅ Uuendame rippmenüüd KOHE!

            # Tühjendame sisestuskastid
            self.view.get_txt_word.delete(0, END)
            self.view.get_txt_category.delete(0, END)
        else:
            messagebox.showwarning("Viga", "Palun sisesta sõna ja vali kategooria!")

    def update_word(self):
        """
        Uuendab valitud sõna andmebaasis.
        """
        selected_item = self.view.get_my_table.selection()
        if not selected_item:
            messagebox.showwarning("Viga", "Palun vali sõna, mida muuta!")
            return

        # Võtame ID, vana sõna ja vana kategooria
        values = self.view.get_my_table.item(selected_item, "values")
        word_id = values[1]  # ID veerg

        # Võtame uued väärtused kasutaja sisestusest
        new_word = self.view.get_txt_word.get().strip()
        new_category = self.view.get_txt_category.get().strip()

        if new_word and new_category:
            # Uuendame andmebaasi
            self.model.update_word(int(word_id), new_word, new_category)

            # Värskendame tabelit
            self.update_table()
        else:
            messagebox.showwarning("Viga", "Palun sisesta uus sõna ja kategooria!")

    def delete_word(self):
        """
        Kustutab valitud sõna andmebaasist.
        """
        selected_item = self.view.get_my_table.selection()
        if not selected_item:
            messagebox.showwarning("Viga", "Palun vali sõna, mida kustutada!")
            return

        word_id = self.view.get_my_table.item(selected_item, "values")[1]  # ID
        self.model.delete_word(int(word_id))
        self.update_table()

    def update_table(self):
        """
        Värskendab tabelit ja kuvab andmebaasi sisu otse andmebaasist.
        """
        self.view.get_my_table.delete(*self.view.get_my_table.get_children())  # Tühjendame tabeli

        words = self.model.db.get_all_words()  # Võtame andmebaasi andmed otse

        print(f"DEBUG: Andmed enne GUI värskendamist: {words}")  # Kontrollime, kas andmed jõuavad siia

        if not words:
            print("ERROR: Andmebaasis pole ühtegi sõna!")

        for i, (word_id, word, category) in enumerate(words, start=1):
            self.view.get_my_table.insert("", "end", values=(i, word_id, word, category))

        self.update_category_combobox()  # Uuendame ka kategooriate rippmenüü!


    def combobox_change(self, event=None):
        """
        Kui valitakse rippmenüüst tegevus, saadakse kätte tekst kui ka index (print lause). Näide kuidas võiks
        rippmenüü antud rakenduses töötada :)
        :param event: vaikimisi pole
        :return: None
        """
        if self.view.get_combo_categories.current() > 0:  # Vali kategooria on 0
            self.view.get_txt_category.delete(0, END)  # Tühjenda uue kategooria sisestuskast
            self.view.get_txt_category.config(state='disabled')  # Ei saa sisestada uut kategooriat
            self.view.get_txt_word.focus()
        else:
            self.view.get_txt_category.config(state='normal')  # Saab sisestada uue kategooria
            self.view.get_txt_category.focus()

    def open_database(self):
        """
        Avab kasutaja valitud andmebaasi ja kontrollib, kas see sisaldab 'words' tabelit.
        Kui mitte, loob uue 'hangman_2025.db' koos õige struktuuriga.
        """
        db_path = askopenfilename(title="Vali andmebaas", filetypes=[("SQLite Database", "*.db")])

        if not db_path:  # Kui kasutaja vajutab "Cancel", siis ei tehta midagi
            return

        print(f"DEBUG: Kasutaja valis andmebaasi: {db_path}")

        # Loome uue Database objekti uue failiga
        self.model.db = Database(db_path)

        # Kontrollime, kas valitud andmebaasis on tabel 'words'
        self.model.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words'")
        result = self.model.db.cursor.fetchone()

        if not result:
            messagebox.showwarning("Viga", "Valitud andmebaasis puudub vajalik tabel. Luuakse uus andmebaas!")
            os.remove(db_path)  # Kustutame vigase faili
            self.model.db = Database()  # Loome uue 'hangman_2025.db' vaikimisi

        self.update_table()  # Uuendame tabeli

    def update_word_directly(self, word_id, new_word=None, new_category=None):
        """
        Otsene andmete muutmine tabelist.
        """
        if new_word:
            self.model.update_word(word_id, new_word,
                                   self.model.db.cursor.execute("SELECT category FROM words WHERE id = ?",
                                                                (word_id,)).fetchone()[0])
        if new_category:
            self.model.update_word(word_id, self.model.db.cursor.execute("SELECT word FROM words WHERE id = ?",
                                                                         (word_id,)).fetchone()[0], new_category)
        self.update_table()

    def update_category_combobox(self):
        """
        Värskendab rippmenüüd andmebaasis olevate unikaalsete kategooriatega.
        """
        categories = self.model.db.get_all_categories()  # Pärib kategooriad otse andmebaasist

        print(f"DEBUG: update_category_combobox() tulemused: {categories}")  # Kontrollime, kas "Värvid" on siin!

        if not categories:
            categories = ["- Kategooriad puuduvad -"]  # Kui andmebaasis pole ühtegi kategooriat

        self.view.get_combo_categories['values'] = ["Vali kategooria"] + categories
        self.view.get_combo_categories.current(0)  # Seame vaikimisi esimese valiku






