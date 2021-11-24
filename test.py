import json
import random
import tkinter
from difflib import get_close_matches
from tkinter import *
from tkinter import Menu
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import sys
import os
row = 0
column = 0
color_1 = "#52595D"    #grey


class App(tkinter.Tk):
    def __init__(self):

        Tk.__init__(self)

        menubar = Menu()

        self.menubar =Menu(menubar)

        self.fileMenu = Menu(self.menubar,tearoff=0)
        self.fileMenu.add_command(label="Data List",command= lambda : self.create_new_window())
        self.fileMenu.add_command(label="Exit",command=self.exit)

        self.fileMenu.add_command(label="Delete the Whole Data",command= self.delete_json)

        self.menubar.add_cascade(label="File",underline=0, menu=self.fileMenu)
        self.config(menu=self.menubar)

        self.canvas = Canvas(width=500, height=300,bg="#52595D", highlightthickness=0)
        self.logo_png = PhotoImage(file="py_resim.png")
        self.canvas.create_image(300,200,image= self.logo_png)
        self.canvas.grid(row=0, column=1)

        self.word_label = Label(text="Word:",font=("Georgia",15,"bold"),bg=color_1,highlightthickness=0)
        self.word_label.grid(row=1,column=0)

        self.meaning_label = Label(text="Meaning:",font=("Georgia",15,"bold"),bg=color_1,highlightthickness=0)
        self.meaning_label.grid(row=2,column=0)

        self.tr_label = Label(text="Turkish Meaning:",font=("Georgia",15,"bold"),bg=color_1,highlightthickness=0)
        self.tr_label.grid(row=3,column=0)

        self.example_label = Label(text="Examples:",font=("Georgia",15,"bold"),bg=color_1,highlightthickness=0)
        self.example_label.grid(row=4,column=0)

        self.word_input = Entry()
        self.word_input.grid(row=1,column=1,sticky="EW")

        self.meaning_input = Entry()
        self.meaning_input.grid(row=2,column=1,sticky="EW")

        self.tr_input = Entry()
        self.tr_input.grid(row=3,column=1,sticky="EW")

        self.exmpl_input = Entry()
        self.exmpl_input.grid(row=4,column=1,sticky="EW")

        self.save_button = Button(text="Save",width=20,font=("Georgia",15,"bold"),bg="yellow",command= self.save_info)
        self.save_button.grid(row=5,column=1)

        self.get_meaning_button = Button(text="Generate",width=15,font=("Georgia",10,"bold"),bg="blue",
                                         command=self.generate_meaning)
        self.get_meaning_button.grid(row=1,column=5)

        self.guess = Label(text="Guess the word:",font=("Georgia", 15, "bold"),bg=color_1,highlightthickness=0)
        self.guess.grid(row=3,column=4)

        self.guess_input = Entry()
        self.guess_input.grid(row=3,column=5,sticky="EW")

        self.get_meaning_label = Label(text="Generated Meaning:",font=("Georgia",15,"bold"),
                                       bg=color_1,highlightthickness=0)
        self.get_meaning_label.grid(row=2,column=4)

        self.get_meaning_text = Text(height=4,width=30)

        self.get_meaning_text.grid(row=2,column=5,sticky="EW")

        self.guess_button = Button(text="Guess",width=20,font=("Georgia",15,"bold"),bg="green",
                                   command= self.guess_meaning)
        self.guess_button.grid(row=4,column=5)

        self.hint_button = Button(text="💡\nHint",bg="yellow",font=("Georgia",7),command=self.hint)
        self.hint_button.grid(row=3,column=6)

        self.button_clicked = 0  # default

        self.db_connect()  #db connection

    def db_connect(self):
        self.con = mysql.connector.connect(
            host="localhost",
            username="root",
            password="python123",
            database="dictionary_testing"
        )
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS dictionary_testing")
        self.con.commit()
        self.create_table()

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS Words (
                    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    WORD VARCHAR(255) NOT NULL,
                    ENG_MEANING VARCHAR(255) NOT NULL,
                    TR_MEANING VARCHAR(255) NOT NULL,
                    EXAMPLES VARCHAR(255) NOT NULL
                )
                """
        self.cursor.execute(query)


    def save_info(self):
        self.word = self.word_input.get()
        self.eng_meaning = self.meaning_input.get()
        self.tr_meaning = self.tr_input.get()
        self.example = self.exmpl_input.get()

        self.new_data = {
            self.word:{
                "eng_definition": self.eng_meaning,
                "tr_definition": self.tr_meaning,
                "examples": self.example,
        }
        }


        if len(self.word) == 0 or len(self.eng_meaning) == 0 or len(self.tr_meaning) == 0 or len(self.example) == 0:
            messagebox.showwarning(title="Empty Area",message="All of the boxes must be filled!")

        else:

            try:

                with open("data_test.json", "r", encoding="utf-8") as file:
                    data = json.load(file)

            except (FileNotFoundError,json.decoder.JSONDecodeError):

                with open("data_test.json", "w", encoding="utf-8") as file:
                    json.dump(self.new_data,file,indent=4,ensure_ascii=False)

                    self.con.cursor()
                    query = "INSERT INTO Words(WORD,ENG_MEANING,TR_MEANING,EXAMPLES) VALUES (%s,%s,%s,%s)"
                    values = (self.word,self.eng_meaning,self.tr_meaning,self.example)
                    self.cursor.execute(query,values)
                    self.con.commit()

                    messagebox.showinfo(title="Successfully Added",
                                        message="Your information has been successfully added.")


            else:

                if self.word in data.keys():
                    data.update(self.new_data)
                    accept_change = messagebox.askyesno(title="Existing Word",
                                                        message=f"The word '{self.word}' already exists. Do you want to change it ?")

                    if accept_change:
                        with open("data_test.json", "w", encoding="utf-8") as file:
                            json.dump(data,file,indent=4,ensure_ascii=False)


                            query_1 = "UPDATE Words SET WORD = %s,ENG_MEANING = %s,TR_MEANING = %s,EXAMPLES = %s WHERE WORD = %s"
                            self.cursor.execute(query_1,(self.word,self.eng_meaning,self.tr_meaning,self.example,self.word))
                            self.con.commit()

                            messagebox.showinfo(title="Successfully Changed",
                                                message="Your information has been successfully changed!")

                    else:
                        pass

                else:
                    data.update(self.new_data)
                    with open("data_test.json", "w", encoding="utf-8") as file:
                        json.dump(data,file,indent=4,ensure_ascii=False)

                        messagebox.showinfo(title="Successfully Added",
                                            message="Your information has been successfully added!")

        #INSERTING DATA ////

                        query = "INSERT INTO Words(WORD,ENG_MEANING,TR_MEANING,EXAMPLES) VALUES (%s,%s,%s,%s)"
                        self.values = (self.word,self.eng_meaning,self.tr_meaning,self.example)


                        self.cursor.execute(query,self.values)
                        self.con.commit()


            finally:
                self.word_input.delete(0,"end")
                self.meaning_input.delete(0,"end")
                self.tr_input.delete(0,"end")
                self.exmpl_input.delete(0,"end")


    def generate_meaning(self):

        try:
            with open("data_test.json", "r", encoding="utf-8") as file:
                data = json.load(file)

        except (FileNotFoundError,json.decoder.JSONDecodeError):

            messagebox.showinfo(title="Error",message="No Data File Found.")

        else:
            with open("data_test.json", "r") as file:
                data = json.load(file)

            temp = "eng_definition"
            self.result = [i[temp] for i in data.values() if temp in i.keys()]

            self.random_meanings = [random.choice(self.result)]

            self.text_info = self.get_meaning_text.get("1.0","end")

            if len(self.guess_input.get()) > 0:
                self.guess_input.delete(0,"end")

            if len(self.text_info) > 0:

                self.get_meaning_text.delete("1.0","end")
                self.button_clicked = 0
                for _ in self.random_meanings:
                    self.get_meaning_text.insert(END, _)
                    self.button_clicked = 0
            else:
                self.button_clicked = 0

                for _ in self.random_meanings:
                    self.get_meaning_text.insert(END, _)

    def guess_meaning(self):

        self.get_the_meaning = self.get_meaning_text.get("1.0","end")
        self.your_guess = self.guess_input.get()

        try:
            with open("data_test.json", "r", encoding="utf-8") as file:
                data = json.load(file)

        except (FileNotFoundError,json.decoder.JSONDecodeError):

            messagebox.showinfo(title="Error",message="No Data File Found.")

        else:
            with open("data_test.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            try:

                if data[self.your_guess]["eng_definition"] in self.get_the_meaning:

                    messagebox.showinfo(title="Well Done!",message="Nice Job.")
                    self.get_meaning_text.delete("1.0","end")
                    self.guess_input.delete(0,"end")
                    self.button_clicked = 0

                else:
                    messagebox.showinfo(title="Try Again",
                                        message="Wrong guess, but this word does exist in your dictionary.")

            except KeyError:

                if len(self.your_guess) > 0:

                    if str(self.your_guess).upper() in data:
                        self.guess_input.delete(0,"end")
                        self.guess_input.insert(0,self.your_guess.upper())

                    elif self.your_guess.lower() in data:
                        self.guess_input.delete(0,"end")
                        self.guess_input.insert(0,self.your_guess.lower())

                    elif str(self.your_guess).capitalize() in data:
                        self.guess_input.delete(0,"end")
                        self.guess_input.insert(0,str(self.your_guess).capitalize())

                    elif len(get_close_matches(self.your_guess.title(),data.keys())) > 0:
                        the_closer = get_close_matches(str(self.your_guess).title(),data.keys())[0]
                        y_or_n = messagebox.askyesno(message=f"Did you mean {the_closer} instead?")

                        if y_or_n:
                            self.guess_input.delete(0,"end")
                            self.guess_input.insert(0,the_closer)

                        else:
                            close_words = []
                            a = get_close_matches(self.your_guess.title(),data.keys())

                            for i in a:
                                close_words.append(i)

                            y_or_n_2 = messagebox.askyesno(message=f"Close Words : {close_words}. Is the word in the list?")

                            if y_or_n_2:
                                pass

                            else:
                                messagebox.showwarning(message="Try to spell the word correctly.")

                    else:
                        messagebox.showwarning(message="No such word found in the dictionary.")

                else:
                    messagebox.showwarning(title="Empty Box",message="You have to guess a word.")

    def hint(self):

        self.get_text = self.get_meaning_text.get("1.0","end")
        your_guess = self.guess_input.get()

        try:
            with open("data_test.json", "r", encoding="utf-8") as file:
                data = json.load(file)

        except (FileNotFoundError, json.decoder.JSONDecodeError):

            messagebox.showinfo(title="Error", message="No Data File Found.")

        else:
            with open("data_test.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            for i in list(data.items()):

                if i[1]["eng_definition"] in self.get_text:

                    global str_word
                    str_word = ""
                    if len(your_guess) == 0:
                        try:
                            self.button_clicked = 0
                            str_word += i[0][self.button_clicked]
                            self.guess_input.insert(0,str_word)


                        except IndexError:
                            self.button_clicked = 0

                    else:  # len(your_guess) > 0

                        try:
                            self.button_clicked += 1
                            str_word += i[0][self.button_clicked]
                            self.guess_input.insert(self.button_clicked,str_word)



                        except IndexError:

                            break


    def create_new_window(self):   # Data list window
        self.new_wd = Toplevel()
        self.new_wd.title("Data Info/Inserting")

        self.new_wd.geometry("900x500")

        self.initUI()

        self.new_wd.mainloop()

#***************************************************************************************
    def initUI(self):

        self.tv = ttk.Treeview(self.new_wd, columns= (1,2,3,4), show= "headings",height=25)

        style = ttk.Style()
        style.configure("Treeview",background="silver",
                        foreground="black",
                        )
        style.map("Treeview",background=[("selected","green")])

        self.tv.column(1,width=150)
        self.tv.column(2,width=800)
        self.tv.column(3,width=400)
        self.tv.column(4,width=800)
        self.tv.heading(1, text= "Word")
        self.tv.heading(2, text="Meaning")
        self.tv.heading(3, text="Tr Meaning")
        self.tv.heading(4, text="Example")

        self.scrollbar = Scrollbar(self.new_wd, orient = VERTICAL, command= self.tv.yview)
        self.scrollbar.config(command= self.tv.yview)
        self.scrollbar.pack(side= RIGHT,fill= Y)
        self.tv.configure(yscroll= self.scrollbar.set)

        self.scrollbar = Scrollbar(self.new_wd, orient= HORIZONTAL, command= self.tv.xview)
        self.scrollbar.config(command= self.tv.xview)
        self.scrollbar.pack(side= BOTTOM, fill=X)
        self.tv.configure(xscroll= self.scrollbar.set)

        self.tv.pack()


        try:
            with open("data_test.json", "r", encoding="utf-8") as file:
                data = json.load(file)

        except (FileNotFoundError, json.decoder.JSONDecodeError):

            pass


        else:

            with open("data_test.json", "r", encoding="utf-8") as file:
               data = json.load(file)


            data_set = []
            for i in list(data.items()):
                data_set.append((i[0],i[1]["eng_definition"],i[1]["tr_definition"],i[1]["examples"]))


            for j in data_set:
                self.tv.insert('',END,values= j)


    def exit(self):
        sys.exit(0)


    def delete_json(self):

        yes_no = messagebox.askyesno(title="Warning",message="Do you want to apply this change? This may cause data loss.")
        if yes_no:
            os.remove("data_test.json")
            query = "TRUNCATE TABLE Words"
            self.cursor.execute(query)
            self.con.commit()

if __name__ == "__main__":
    window = App()
    window.wm_resizable(False,False)
    photo = PhotoImage(file="logopy.png")
    window.iconphoto(False,photo)
    window.title("B&B English Dictionary and Quiz App")
    window.configure(width=1000,height=1000,bg= "#52595D" )
    window.config(padx=20,pady=20)
    window.mainloop()
