from tkinter import Button, Canvas, Entry, Frame, Label, Listbox, Tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from os.path import isfile
from random import randint


class MainWindow:
    def __init__(self):
        self.__INTERFACE_FONT = "Consolas 10"
        self.__QUESTIONS_FONT = "Consolas 20"
        self.__topics = {}
        self.__answer = ""
        self.__window = Tk()
        self.__window.title("Quizz")
        self.__window.resizable(width=False, height=False)
        left_frame = Frame(
            self.__window,
            bd=0
        )
        left_frame.grid(row=0, column=0, sticky="nw")
        Label(
            left_frame,
            text="Chemin du fichiers des questions : ",
            font=self.__INTERFACE_FONT
        ).grid(row=0, column=0, sticky="w")
        self.__button_browse = Button(
            left_frame,
            text="Parcourir",
            font=self.__INTERFACE_FONT,
            command=self.__browse_file
        )
        self.__button_browse.grid(row=1, column=0, sticky="w")
        frame = Frame(
            left_frame,
            bd=0
        )
        frame.grid(row=2, column=0, sticky="w")
        self.__entry_file = Entry(
            frame,
            font=self.__INTERFACE_FONT,
            width=30
        )
        self.__entry_file.grid(row=0, column=0, sticky="w")
        self.__entry_file.bind("<Key>", self.__file_modification)
        self.__label_modification = Label(
            frame,
            text="*",
            font=self.__INTERFACE_FONT
        )
        self.__label_modification.grid(row=0, column=1, sticky="w")
        self.__button_validate = Button(
            frame,
            text="►",
            font=self.__INTERFACE_FONT,
            command=self.__load_file
        )
        self.__button_validate.grid(row=0, column=2, sticky="w")
        Label(
            left_frame,
            text="Thèmes :",
            font=self.__INTERFACE_FONT
        ).grid(row=3, column=0, sticky="w")
        self.__listbox_topics = Listbox(
            left_frame,
            font=self.__INTERFACE_FONT,
            width=35,
            height=20
        )
        self.__listbox_topics.grid(row=4, column=0, sticky="w")
        self.__listbox_topics.bind("<Button-1>", self.__change_color)
        self.__button_reset = Button(
            left_frame,
            text="Réinitialiser les questions",
            font=self.__INTERFACE_FONT,
            command=self.__reset_questions
        )
        self.__button_reset.grid(row=5, column=0, sticky="w")
        Label(
            left_frame,
            text="Question :",
            font=self.__INTERFACE_FONT
        ).grid(row=6, column=0, sticky="w")
        frame = Frame(
            left_frame,
            bd=0
        )
        frame.grid(row=7, column=0, sticky="w")
        self.__listbox_question = Listbox(
            frame,
            font=self.__INTERFACE_FONT,
            width=30,
            height=1
        )
        self.__listbox_question.grid(row=0, column=0, sticky="w")
        self.__button_question = Button(
            frame,
            text="►",
            font=self.__INTERFACE_FONT,
            command=self.__show_question
        )
        self.__button_question.grid(row=0, column=1, sticky="w")
        Label(
            left_frame,
            text="Temps de réponse (en s) :",
            font=self.__INTERFACE_FONT
        ).grid(row=8, column=0, sticky="w")
        self.__entry_time = Entry(
            left_frame,
            font=self.__INTERFACE_FONT,
            width=10
        )
        self.__entry_time.grid(row=9, column=0, sticky="w")
        self.__entry_time.insert(0, "60")
        self.__button_show = Button(
            left_frame,
            text="Afficher la réponse",
            font=self.__INTERFACE_FONT,
            command=self.__show_answer
        )
        self.__button_show.grid(row=10, column=0, sticky="w")
        self.__canvas = Canvas(
            self.__window,
            bg="#ffffff",
            width=800,
            height=600
        )
        self.__canvas.grid(row=0, column=1, sticky="nw")
        self.__window.mainloop()

    def __file_modification(self, event):
        if event.keysym == "Return":
            self.__browse_file()
        else:
            self.__label_modification["text"] = "*"

    def __browse_file(self):
        rep = askopenfilename(filetypes=[("Text Files", "*.txt")])
        if rep != "":
            self.__entry_file.delete(0, "end")
            self.__entry_file.insert(0, rep)
            self.__label_modification["text"] = "*"

    def __update_listboxes(self):
        size = self.__listbox_question.size()
        index = self.__listbox_question.nearest(0)
        self.__listbox_topics.delete(0, "end")
        self.__listbox_question.delete(0, "end")
        for i in self.__topics:
            self.__listbox_topics.insert(
                "end",
                "{} {}/{}".format(
                    i,
                    self.__topics[i][2],
                    self.__topics[i][1]
                )
            )
            self.__listbox_topics.itemconfig(
                "end",
                background=self.__topics[i][0]
            )
            self.__listbox_topics.itemconfig(
                "end",
                selectbackground=self.__topics[i][0]
            )
            self.__listbox_topics.itemconfig(
                "end",
                foreground="#000000"
            )
            self.__listbox_topics.itemconfig(
                "end",
                selectforeground="#000000"
            )
            if self.__topics[i][2] > 0:
                self.__listbox_question.insert("end", i)
        self.__listbox_question.insert("end", "Aléatoire")
        if self.__listbox_question.size() == size:
            self.__listbox_question.see(index)

    def __load_file(self):
        if self.__answer != "":
            showerror(
                "Erreur",
                "Vous ne pouvez pas faire ça pendant qu'une question est"
                "posée."
            )
        elif isfile(self.__entry_file.get()):
            for i in list(self.__topics.keys()):
                del self.__topics[i]
            file = open(self.__entry_file.get(), "r", encoding="ansi")
            lines = file.read().split("\n")
            for i in range(0, len(lines)-2, 3):
                topic = lines[i]
                if topic == "Aléatoire":
                    topic += "_"
                if topic in self.__topics:
                    self.__topics[topic][1] += 1
                    self.__topics[topic][2] += 1
                    self.__topics[topic][3] += [[True, lines[i+1], lines[i+2]]]
                else:
                    self.__topics[topic] = [
                        "#ffffff",
                        1,
                        1,
                        [[True, lines[i+1], lines[i+2]]]
                    ]
            file.close()
            self.__label_modification["text"] = " "
            self.__update_listboxes()
        else:
            showerror("Erreur", "Ce fichier n'existe pas.")

    def __change_color(self, event):
        i = self.__listbox_topics.nearest(event.y)
        if i > -1:
            rep = askcolor()[1]
            if rep is not None:
                topic = " ".join(self.__listbox_topics.get(i).split(" ")[:-1])
                self.__topics[topic][0] = rep
                self.__update_listboxes()

    def __reset_questions(self):
        for i in self.__topics:
            self.__topics[i][2] = self.__topics[i][1]
            for j in range(self.__topics[i][1]):
                self.__topics[i][3][j][0] = True
        self.__update_listboxes()

    def __show_question(self):
        try:
            int(self.__entry_time.get())
            if self.__answer != "":
                showerror("Erreur", "Une question est déjà en cours.")
            elif self.__listbox_question.size() == 1:
                showerror("Erreur", "Il n'y a plus de questions disponibles.")
            else:
                topic = self.__listbox_question.get(
                    self.__listbox_question.nearest(0)
                )
                if topic == "Aléatoire":
                    n_topics = self.__listbox_question.size()-1
                    topic = self.__listbox_question.get(randint(0, n_topics-1))
                question = randint(0, self.__topics[topic][2]-1)
                i = 0
                n = 0
                while n <= question:
                    if self.__topics[topic][3][i][0]:
                        n += 1
                    i += 1
                i -= 1
                self.__topics[topic][2] -= 1
                self.__topics[topic][3][i][0] = False
                self.__answer = self.__topics[topic][3][i][2]
                self.__canvas.delete("all")
                self.__canvas["bg"] = self.__topics[topic][0]
                self.__canvas.create_text(
                    int(self.__canvas["width"])/2,
                    int(self.__canvas["height"])/2,
                    text=self.__topics[topic][3][i][1],
                    font=self.__QUESTIONS_FONT,
                    fill="#000000",
                    width=int(self.__canvas["width"])
                )
                self.__update_listboxes()
                self.__show_timer(int(self.__entry_time.get()), None)
        except:
            showerror("Erreur", "Le temps de réponse doit être un entier.")

    def __show_timer(self, n, text):
        if self.__answer != "":
            if text is not None:
                self.__canvas.delete(text)
            text = self.__canvas.create_text(
                int(self.__canvas["width"])/2,
                10,
                anchor="n",
                text=int(n),
                font=self.__QUESTIONS_FONT,
                fill="#000000"
            )
            if n == 0:
                self.__canvas.delete("all")
                self.__canvas.create_text(
                    int(self.__canvas["width"])/2,
                    int(self.__canvas["height"])/2,
                    text="Plus de temps !",
                    font=self.__QUESTIONS_FONT,
                    fill="#000000"
                )
            else:
                self.__canvas.after(
                    1000,
                    lambda x=n-1, y=text: self.__show_timer(x, y)
                )

    def __show_answer(self):
        answer = self.__answer
        self.__answer = ""
        self.__canvas.delete("all")
        self.__canvas.create_text(
            int(self.__canvas["width"])/2,
            int(self.__canvas["height"])/2,
            text=answer,
            font=self.__QUESTIONS_FONT,
            fill="#000000",
            width=int(self.__canvas["width"])
        )


main_window = MainWindow()
