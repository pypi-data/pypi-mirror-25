import pprint
from tkinter import *
from tkinter import filedialog, ttk

import logging
from pymongo import MongoClient
import json
import time
import ast

def do_nothing():
    print("Action Performed")


class DBManager:
    client = None
    db = None

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.fyp

    def insert(self, file_name):
        g = open(file_name, 'r')  # definging open mode
        start_time = time.time()
        count = 0
        current_status.set(str(count) + "Insertion started at \n" + str(start_time))

        for l in g:  # initiallizing loop
            self.db.reviews.insert(l)  # inserting into tables
            count = count + 1
            # print("Inserted " + str(count) + " records total time taken %s seconds" % (time.time() - start_time))

        current_status.set(str(count) + " records inserted in : %s seconds" % (time.time() - start_time))

    def show_all(self):
        start_time = time.time()
        count = 0
        current_status.set("Printing Reviews in Terminal")

        for a in self.db.reviews.find():  # reading all reviews in db
            pprint.pprint(a)  # printing all
            count = count + 1
        current_status.set(str(count) + " records printed in %s seconds..." % (time.time() - start_time))

    def delete_all(self):
        start_time = time.time()
        result = self.db.reviews.delete_many({})  # deleting all records in schema
        current_status.set(
            "Total " + str(result.deleted_count) + " files deleted in %s seconds" % (time.time() - start_time))
        # print(result.deleted_count)


class MyMenu:
    def __init__(self, master):
        menu = Menu(master)
        master.config(menu=menu)

        sub_menu = Menu(menu)
        menu.add_cascade(label="File", menu=sub_menu)
        sub_menu.add_command(label="New Project...", command=do_nothing)
        sub_menu.add_command(label="Open an existing Project...", command=do_nothing)
        sub_menu.add_separator()
        sub_menu.add_command(label="Exit", command=master.quit)

        edit_menu = Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=do_nothing)
        edit_menu.add_command(label="Redo", command=do_nothing)


class MyToolbar:
    def __init__(self, master):
        toolbar = Frame(master, bg="#03A9F4")
        delete_all = Button(toolbar, text="Delete All", fg="black", bg="white", command=lambda: self.delete_all())
        delete_all.pack(side=LEFT, padx=2, pady=2)
        #
        show_all = Button(toolbar, text="Show All", fg="black", bg="white", command=lambda: self.show_all())
        show_all.pack(side=LEFT, padx=2, pady=2)

        toolbar.pack(side=TOP, fill=X)

    @staticmethod
    def show_all():
        print("Showing all...")
        db = DBManager()
        db.show_all()

    @staticmethod
    def delete_all():
        db = DBManager()
        db.delete_all()


class Body:
    def __init__(self, master):
        frame = Frame(master, bg="#BDBDBD", width=400, height=100)
        file_path = Label(frame, textvariable=file, padx=10, pady=5)
        file_path.grid(row=3, columns=1)
        browse = Button(frame, text="Browse", fg="black", bg="white", command=lambda: self.open_browse())
        browse.grid(row=3, column=5)

        # start_insert = Button(frame, text="Start insertion", fg="black", bg="white", command=self.start_insert)
        # start_insert.grid(row=4, column=1)
        #

        frame.pack()

    @staticmethod
    def open_browse():
        filename = filedialog.askopenfilename()
        file.set(filename)
        db = DBManager()
        db.insert(file.get())

        #
        # @staticmethod
        # def start_insert():
        #     db = DBManager()
        #     db.insert(str(file))
        #


class MyStatusBar:
    def __init__(self, master):
        status = Label(master, textvariable=current_status, bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)

root = Tk()
file = StringVar()
current_status = StringVar()
current_status.set("Click Browse and select a file to continue ,,,")
file.set("No File Chosen")


def main():

    menu = MyMenu(root)
    toolbar = MyToolbar(root)
    statusBar = MyStatusBar(root)
    body = Body(root)

    # root.resizable(width=False, height=False)
    root.wm_title("DB Manager")
    root.iconbitmap("favicon.ico")
    root.minsize(width=400, height=100)
    root.maxsize(width=700, height=100)
    root.mainloop()


if __name__ == '__main__':
    main()


