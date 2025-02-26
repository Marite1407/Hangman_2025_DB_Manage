from tkinter import *
from tkinter.ttk import Combobox, Treeview

class View(Tk):

    def __init__(self, model, controller):  # Lisame controlleri parameetrina
        """
        Põhiakna konstruktor
        """
        super().__init__()
        self.model = model
        self.controller = controller  # Seome kontrolleri õigesti

        self.__myTable = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Põhiaken
        self.__width = 400
        self.__height = 300
        self.title('Poomismängu andmebaasi haldus')
        self.center(self, self.__width, self.__height)

        # Paneelid ja põhivormid
        self.__frame_top, self.__frame_bottom, self.__frame_right = self.create_frames()
        self.__lbl_category, self.__txt_category, self.__lbl_word, self.__txt_word = self.create_main_form()
        self.__lbl_old_categories, self.__combo_categories = self.create_combobox()
        self.__btn_add, self.__btn_edit, self.__btn_delete, self.__btn_open = self.create_buttons()
        self.create_table()

        # Seome ENTER-klahvi sõna lisamiseks
        self.bind("<Return>", lambda event: self.controller.add_word(event))


    @staticmethod
    def center(win, w, h):
        """
        Meetod mis paigutab etteantud akna ekraani keskele vastavalt monitori suurusele
        :param win: aken mida paigutada
        :param w:   akna laius
        :param h:   akna kõrgus
        :return:    None
        """
        x = int((win.winfo_screenwidth() / 2) - (w / 2))
        y = int((win.winfo_screenheight() / 2) - (h / 2))
        win.geometry(f'{w}x{h}+{x}+{y}')

    def create_frames(self):
        """
        Loob kaks frame mis paigutatakse põhiaknale (View)
        :return:
        """
        top = Frame(self, height=50, background='lightblue')
        bottom = Frame(self, background='lightyellow')
        right = Frame(top, background='lightgray')

        # Paneme paneelid põhi aknale
        top.pack(fill=BOTH)
        bottom.pack(fill=BOTH, expand=True)
        right.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

        return top, bottom, right # Tagastame loodud paneelid õiges järjekorras

    def create_main_form(self):
        """
        Loob põhi vormi kaks labelit ja kaks sisestuskasti
        :return: lbl_1, txt_1, lbl_2, txt_2
        """
        lbl_1 = Label(self.__frame_top, text='Uus kategooria:', background='lightblue', font=('Verdana', 10, 'bold'))
        txt_1 = Entry(self.__frame_top)
        txt_1.focus()
        lbl_1.grid(row=0, column=0, pady=5, sticky=EW)
        txt_1.grid(row=0, column=1, sticky=EW)

        lbl_2 = Label(self.__frame_top, text='Sõna:', background='lightblue', font=('Verdana', 10, 'bold'))
        lbl_2.grid(row=2, column=0, pady=5, sticky=EW)
        txt_2 = Entry(self.__frame_top)
        txt_2.grid(row=2, column=1, sticky=EW)

        return lbl_1, txt_1, lbl_2, txt_2

    def create_buttons(self):
        """
        Loob nupud CRUD jaoks: Lisa, Muuda, Kustuta ja Ava.
        """
        btn_1 = Button(self.__frame_right, text='Lisa')
        btn_2 = Button(self.__frame_right, text='Muuda')
        btn_3 = Button(self.__frame_right, text='Kustuta')
        btn_4 = Button(self.__frame_right, text='Ava')  # Uus nupp andmebaasi avamiseks

        btn_1.grid(row=0, column=1, padx=1, sticky=EW)
        btn_2.grid(row=1, column=2, padx=1, sticky=EW)
        btn_3.grid(row=0, column=2, padx=1, sticky=EW)
        btn_4.grid(row=1, column=1, padx=1, sticky=EW)  # Paigutame Ava nupu tabelisse

        return btn_1, btn_2, btn_3, btn_4  # Tagastatakse 4 nuppu!

    def create_combobox(self):
        """
        Loob ja tagastab rippmenüü labeli ja rippmenüü enda
        """
        label = Label(self.__frame_top, text='Vana kategooria', background='lightblue', font=('Verdana', 10, 'bold'))
        label.grid(row=1, column=0, pady=5, sticky=EW)

        combo = Combobox(self.__frame_top)
        combo.grid(row=1, column=1, padx=4, sticky=EW)

        return label, combo

    def create_table(self):
        """
        Loob tabeli mis näitab kirjeid (sõnu ja nende kategooriaid). Loodud ainult tabeli päise osa
        :return: None
        """
        self.__myTable = Treeview(self.__frame_bottom)
        self.__myTable.bind("<<TreeviewSelect>>", self.fill_entry_fields)  # Kui valitakse rida, täidab vormi

        vsb = Scrollbar(self.__frame_bottom, orient=VERTICAL, command=self.__myTable.yview)
        vsb.pack(side=RIGHT, fill=Y)
        self.__myTable.configure(yscrollcommand=vsb.set)

        self.__myTable['columns'] = ('jrk', 'id', 'word', 'category')

        self.__myTable.column('#0', width=0, stretch=NO)
        self.__myTable.column('jrk', anchor=W, width=25)
        self.__myTable.column('id', anchor=W, width=50)
        self.__myTable.column('word', anchor=W, width=100)
        self.__myTable.column('category', anchor=W, width=100)

        self.__myTable.heading('#0', text='', anchor=CENTER)
        self.__myTable.heading('jrk', text='Jrk', anchor=CENTER)
        self.__myTable.heading('id', text='ID', anchor=CENTER)
        self.__myTable.heading('word', text='Sõna', anchor=CENTER)
        self.__myTable.heading('category', text='Kategooria', anchor=CENTER)

        # (START) Siin peaks olema andmete tabelisse lisamise või uuendamise koht

        # (LÕPP) Siin peaks olema andmete tabelisse lisamise või uuendamise koht

        self.__myTable.pack(fill=BOTH, expand=True)
        self.__myTable.bind("<Double-1>", self.on_double_click)  # Kui topeltklikid, saad redigeerida

    @property
    def get_buttons(self):
        """
        Tagastab nupu objektid (Lisa, Muuda, Kustuta, Ava).
        :return: List nuppudest
        """
        return [self.__btn_add, self.__btn_edit, self.__btn_delete, self.__btn_open]  # Lisatud "Ava" nupp

    # GETTERS

    @property
    def get_combo_categories(self):
        """
        Tagastab rippmenüü objekti
        :return: Combobox
        """
        return self.__combo_categories

    @property
    def get_txt_category(self):
        """
        Tagastab uue kategooria sisestuskasti objekti
        :return: Entry objekt
        """
        return self.__txt_category

    @property
    def get_my_table(self):
        """
        Meetod on selleks et saaks tabeli objekti mujal kasutada
        :return: tagastab __myTable objekti
        """
        return self.__myTable

    @property
    def get_txt_word(self):
        """
        Tagastab sisestuskasti kuhu saab sisestada sõna
        :return: Entry objekt
        """
        return self.__txt_word

    def fill_entry_fields(self, event):
        """
        Kui kasutaja klikib tabelis sõnale, täidetakse sisestusväljad automaatselt valitud sõnaga.
        """
        selected_item = self.__myTable.selection()
        if selected_item:
            word_id, word, category = self.__myTable.item(selected_item, "values")[1:4]
            self.__txt_category.delete(0, END)
            self.__txt_category.insert(0, category)
            self.__txt_word.delete(0, END)
            self.__txt_word.insert(0, word)

    def on_double_click(self, event):
        """
        Kui kasutaja topeltklikib tabeli lahtril, saab seda muuta.
        Vajutades ENTER, salvestatakse muudatus andmebaasi.
        """
        item = self.__myTable.selection()
        if not item:
            return

        col = self.__myTable.identify_column(event.x)  # Millise veeru peal klikiti
        row_id = self.__myTable.item(item, "values")[1]  # ID veerg
        selected_value = self.__myTable.item(item, "values")[int(col[1])]

        entry_edit = Entry(self.__frame_bottom)
        entry_edit.insert(0, selected_value)
        entry_edit.place(x=event.x_root - self.__frame_bottom.winfo_rootx(),
                         y=event.y_root - self.__frame_bottom.winfo_rooty())

        def save_edit(event):
            new_value = entry_edit.get().strip()
            entry_edit.destroy()

            if col == "#3":  # Kui muudeti sõna veergu
                self.controller.update_word_directly(row_id, new_value, None)
            elif col == "#4":  # Kui muudeti kategooria veergu
                self.controller.update_word_directly(row_id, None, new_value)

        entry_edit.bind("<Return>", save_edit)  # ENTER vajutamisel salvestame uue väärtuse

        def fill_entry_fields(self, event):
            """
            Kui kasutaja klikib tabelis sõnale, täidetakse sisestusväljad automaatselt valitud sõnaga.
            """
            selected_item = self.__myTable.selection()
            if selected_item:
                values = self.__myTable.item(selected_item, "values")  # Võtab tabelist valitud rea andmed
                if values:
                    word_id, word, category = values[1], values[2], values[3]  # ID, sõna, kategooria
                    self.__txt_category.delete(0, END)
                    self.__txt_category.insert(0, category)
                    self.__txt_word.delete(0, END)
                    self.__txt_word.insert(0, word)


