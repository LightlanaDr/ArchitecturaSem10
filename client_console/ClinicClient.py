import sqlite3
from tkinter import ttk
import tkinter as tk
from tkinter import *


class ClinicClient(tk.Tk):
    db_name = 'ClinicService.db'

    def __init__(self, window):
        super().__init__()
        self.wind = window

        frame = tk.LabelFrame(self.wind, text='Добавить клиента')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        Label(frame, text='Документ: ').grid(row=1, column=0)
        self.document = Entry(frame)
        self.document.focus()
        self.document.grid(row=1, column=1)

        Label(frame, text='Имя: ').grid(row=2, column=0)
        self.surName = Entry(frame)
        self.surName.focus()
        self.surName.grid(row=2, column=1)

        Label(frame, text='Фамилия: ').grid(row=3, column=0)
        self.firstName = Entry(frame)
        self.firstName.focus()
        self.firstName.grid(row=3, column=1)

        Label(frame, text='Отчество: ').grid(row=4, column=0)
        self.patronymic = Entry(frame)
        self.patronymic.focus()
        self.patronymic.grid(row=4, column=1)

        Label(frame, text='Дата рождения: ').grid(row=5, column=0)
        self.birthday = Entry(frame)
        self.birthday.focus()
        self.birthday.grid(row=5, column=1)

        # Button Add Product
        ttk.Button(frame, text='Сохранить клиента', command=self.add_client).grid(row=6, columnspan=2, sticky=W + E)

        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Документ', anchor=CENTER)
        self.tree.heading('#1', text='Имя', anchor=CENTER)
        #
        # # Buttons
        ttk.Button(text='DELETE', command=self.delete_client).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text='EDIT', command=self.edit_client).grid(row=5, column=1, sticky=W + E)

        # Filling the Rows
        self.get_clients()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_clients(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM clients'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

        # User Input Validation

    def validation(self):
        return len(self.surName.get()) != 0 and len(self.firstName.get()) != 0

    def add_client(self):
        if self.validation():
            query = 'INSERT INTO clients VALUES(NULL, ?, ?, ?, ?, ?)'
            parameters = (self.document.get(), self.surName.get(),
                          self.firstName.get(), self.patronymic.get(), self.birthday.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Клиент {} добавлен'.format(self.surName.get())
            self.document.delete(0, END)
            self.surName.delete(0, END)
            self.firstName.delete(0, END)
            self.patronymic.delete(0, END)
            self.birthday.delete(0, END)
        else:
            self.message['text'] = 'Укажите данные'
        self.get_clients()

    def delete_client(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Пожалуйста, выберите запись'
            return
        self.message['text'] = ''
        document = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM clients WHERE document = ?'
        self.run_query(query, (document,))
        self.message['text'] = 'Запись {} удалена'.format(document)
        self.get_clients()

    def edit_client(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        document = self.tree.item(self.tree.selection())['text']
        old_surName = self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Изменить запись'

        Label(self.edit_wind, text='Документ:').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=document), state='readonly').grid(row=0,
                                                                                                             column=2)

        Label(self.edit_wind, text='New документ:').grid(row=1, column=1)
        new_document = Entry(self.edit_wind)
        new_document.grid(row=1, column=2)

        Label(self.edit_wind, text='Имя:').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_surName), state='readonly').grid(row=2,
                                                                                                                column=2)
        # New Price
        Label(self.edit_wind, text='New имя:').grid(row=3, column=1)
        new_surName = Entry(self.edit_wind)
        new_surName.grid(row=3, column=2)

        Button(self.edit_wind, text='Обновить',
               command=lambda: self.edit_records(new_document.get(), document, new_surName.get(), old_surName)).grid(
            row=4, column=2, sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_document, document, new_surName, old_surName):
        query = ('UPDATE clients SET document = ?, surName = ?'
                 'WHERE document = ? AND surName = ?')
        parameters = (new_document, new_surName, document, old_surName)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Запись клиента {} обновлена'.format(new_surName)
        self.get_clients()


if __name__ == '__main__':
    window = Tk()
    window.title("ClinicClient")
    application = ClinicClient(window)
    window.mainloop()
