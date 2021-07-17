#
#   This file contains the Tkinter based GUI
#

import os
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, filedialog
import data
import common
import random

display_options = ["All", "Non-Skipped", "Skipped"]


class TkinterGui:
    def __init__(self, master):

        # variables
        self.master = master
        master.title("Flashcards v1.1")
        self.currentcard = 0

        self.tk_autonext = tk.BooleanVar()
        self.tk_autonext.set(False)
        self.tk_peek = tk.BooleanVar()
        self.tk_peek.set(False)

        # get screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # main rows/columns
        master.columnconfigure(0, weight=1, minsize=200)
        master.columnconfigure(1, weight=1, minsize=200)
        master.rowconfigure(0, minsize=400, weight=16)
        master.rowconfigure(1, minsize=40, weight=1)
        master.rowconfigure(2, minsize=160, weight=4)

        # setup frames
        self.frame_qa = tk.LabelFrame(
            master, borderwidth=4, relief="groove", text=" Questions & Answers "
        )
        self.frame_qa.grid(
            padx=10,
            pady=10,
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
        )

        self.frame_btns = tk.LabelFrame(
            master,
            borderwidth=4,
            relief="groove",
            text="",
        )
        self.frame_btns.grid(
            padx=10, pady=25, row=1, column=0, columnspan=2, sticky="nsew"
        )
        self.frame_btns.columnconfigure(0, weight=1)
        self.frame_btns.columnconfigure(1, weight=1)
        self.frame_btns.columnconfigure(2, weight=1)
        self.frame_btns.columnconfigure(3, weight=1)
        self.frame_btns.columnconfigure(4, weight=1)
        self.frame_btns.columnconfigure(5, weight=1)
        self.frame_btns.columnconfigure(6, weight=1)
        self.frame_btns.columnconfigure(7, weight=1)
        self.frame_btns.columnconfigure(8, weight=1)
        self.frame_btns.columnconfigure(9, weight=1)

        self.frame_stats = tk.LabelFrame(
            master,
            borderwidth=4,
            relief="groove",
            text=" Statistics ",
        )
        self.frame_stats.grid(padx=10, pady=10, row=2, column=0, sticky="nsew")

        self.frame_options = tk.LabelFrame(
            master,
            borderwidth=4,
            relief="groove",
            text=" Options ",
        )
        self.frame_options.grid(padx=10, pady=10, row=2, column=1, sticky="nsew")

        # qa section
        lbl_hide_qa0 = tk.Label(self.frame_qa, text=" ", width=8, font=("Helvetica", 4))
        lbl_hide_qa0.grid(sticky="ew", row=0)

        lbl_topic = tk.Label(self.frame_qa, text="Topic")
        lbl_topic.grid(row=1, column=0, sticky="nw", padx=5, pady=5)

        lbl_section = tk.Label(self.frame_qa, text="Subject")
        lbl_section.grid(row=2, column=0, sticky="nw", padx=5, pady=5)

        lbl_question = tk.Label(self.frame_qa, text="Question")
        lbl_question.grid(row=3, sticky="nw", padx=5, pady=5)

        lbl_answer = tk.Label(self.frame_qa, text="Answer")
        lbl_answer.grid(row=4, column=0, sticky="nw", padx=5, pady=5)

        lbl_hide_qa1 = tk.Label(self.frame_qa, text=" ", width=8, font=("Helvetica", 4))
        lbl_hide_qa1.grid(sticky="ew", row=8)

        self.txt_topic = tk.Text(self.frame_qa, height=1, bg="lemon chiffon", width=160)
        self.txt_topic.grid(row=1, column=1, sticky="nw", padx=5, pady=5)

        self.txt_section = tk.Text(
            self.frame_qa, height=1, bg="lemon chiffon", width=160
        )
        self.txt_section.grid(
            row=2, column=1, sticky="nw", padx=5, pady=5, columnspan=8
        )

        self.txt_question = tk.Text(
            self.frame_qa, height=1, bg="lemon chiffon", width=160
        )
        self.txt_question.grid(
            row=3, column=1, sticky="nw", padx=5, pady=5, columnspan=8
        )

        ch = common.ini["height"]
        cw = common.ini["width"]
        self.txt_answer = tk.Text(
            self.frame_qa, height=ch, bg="lemon chiffon", width=cw, wrap=tk.WORD
        )
        self.txt_answer.grid(row=4, column=1, sticky="nw", padx=5, pady=5, columnspan=8)

        # stats section
        lbl_hide_stat0 = tk.Label(
            self.frame_stats, text=" ", width=8, font=("Helvetica", 4)
        )
        lbl_hide_stat0.grid(sticky="ew", row=0)

        lbl_totq = tk.Label(self.frame_stats, text="Total questions")
        lbl_totq.grid(row=1, sticky="nw", padx=5, pady=1)

        self.txt_totq = tk.Text(self.frame_stats, height=1, bg="lemon chiffon", width=8)
        self.txt_totq.grid(row=1, column=1, sticky="nw", padx=10, pady=1)

        lbl_skipped = tk.Label(self.frame_stats, text="Skipped")
        lbl_skipped.grid(row=2, sticky="nw", padx=15, pady=1)

        self.txt_skipped = tk.Text(
            self.frame_stats, height=1, bg="lemon chiffon", width=8
        )
        self.txt_skipped.grid(row=2, column=1, sticky="nw", padx=10, pady=1)

        lbl_thup = tk.Label(self.frame_stats, text="Thumbs up")
        lbl_thup.grid(row=3, sticky="nw", padx=15, pady=1)

        self.txt_thup = tk.Text(self.frame_stats, height=1, bg="lemon chiffon", width=8)
        self.txt_thup.grid(row=3, column=1, sticky="nw", padx=10, pady=1)

        lbl_thdn = tk.Label(self.frame_stats, text="Thumbs down")
        lbl_thdn.grid(row=4, sticky="nw", padx=15, pady=1)

        self.txt_thdn = tk.Text(self.frame_stats, height=1, bg="lemon chiffon", width=8)
        self.txt_thdn.grid(row=4, column=1, sticky="nw", padx=10, pady=1)

        lbl_currq = tk.Label(self.frame_stats, text="Current/Selected")
        lbl_currq.grid(column=0, row=5, sticky="nw", padx=5, pady=1)

        self.txt_currq = tk.Text(
            self.frame_stats, height=1, bg="lemon chiffon", width=8
        )
        self.txt_currq.grid(row=5, column=1, sticky="nw", padx=10, pady=1)

        lbl_hide_stat1 = tk.Label(
            self.frame_stats, text=" ", width=8, font=("Helvetica", 4)
        )
        lbl_hide_stat1.grid(sticky="ew", row=6)

        lbl_hide_stat2 = tk.Label(
            self.frame_stats, text=" ", width=8, font=("Helvetica", 4)
        )
        lbl_hide_stat2.grid(sticky="ew", row=8)

        # options section
        lbl_hide_opt0 = tk.Label(
            self.frame_options, text=" ", width=8, font=("Helvetica", 4)
        )
        lbl_hide_opt0.grid(sticky="ew", row=0)

        lbl_file_opt = tk.Label(self.frame_options, text="File")
        lbl_file_opt.grid(row=1, sticky="w", padx=5, pady=1)

        lbl_hide_opt1 = tk.Label(
            self.frame_options, text=" ", width=8, font=("Helvetica", 4)
        )
        lbl_hide_opt1.grid(sticky="ew", row=5)

        lbl_display = tk.Label(self.frame_options, text="Display     ")
        lbl_display.grid(row=6, sticky="w", padx=5, pady=1)

        self.txt_file = tk.Text(
            self.frame_options, height=1, bg="lemon chiffon", width=80
        )
        self.txt_file.grid(row=3, column=1, sticky="w", padx=5, pady=1, columnspan=3)

        self.quit_button = tk.Button(
            self.frame_options, text="Quit", command=master.quit
        )
        self.quit_button.grid(row=1, column=3, padx=5, pady=1, sticky="e")

        self.load_button = tk.Button(
            self.frame_options, text="Open File", command=self.load_file
        )
        self.load_button.grid(row=1, column=1, sticky="nw", padx=5, pady=1)

        self.clear_button = tk.Button(
            self.frame_options, text="Clear Results", command=self.clear
        )
        self.clear_button.grid(row=1, column=2, sticky="nw", padx=5, pady=1)

        self.display_cb = ttk.Combobox(self.frame_options)
        self.display_cb["values"] = ["All", "Non-Skipped", "Skipped"]
        self.display_cb["state"] = "readonly"
        self.display_cb.current(1)
        self.display_cb.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        self.display_cb.bind("<<ComboboxSelected>>", self.callback_display)

        self.autonext_ckb = tk.Checkbutton(
            self.frame_options,
            text="Auto-Next on \U0001f44D \U0001f44E",
            onvalue=1,
            offvalue=0,
            variable=self.tk_autonext,
            command=self.callback_autonext,
        )
        self.autonext_ckb.grid(row=6, column=2, sticky="w", padx=5, pady=1)

        self.peek_ckb = tk.Checkbutton(
            self.frame_btns,
            text="Peekmode",
            onvalue=1,
            offvalue=0,
            variable=self.tk_peek,
            command=self.callback_peek,
        )
        self.peek_ckb.grid(row=0, column=8, pady=5, sticky="nse")

        lbl_display = tk.Label(self.frame_options, text="Search     ")
        lbl_display.grid(row=7, sticky="sw", padx=5, pady=1)

        # button section

        # create frames to group some buttons and allow to keep them together
        self.f1 = tk.Frame(self.frame_btns)
        self.f2 = tk.Frame(self.frame_btns)
        self.f1.grid(row=0, column=1, sticky="nsw", pady=5)
        self.f2.grid(row=0, column=4, sticky="nsw", pady=5)

        self.prev_button = tk.Button(self.f1, text="<<", command=self.previous)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.f1, text=">>", command=self.next)
        self.next_button.pack(side=tk.LEFT)

        self.rnd_button = tk.Button(self.f1, text="Random", command=self.random)
        self.rnd_button.pack(side=tk.LEFT)

        self.show_answer_button = tk.Button(
            self.f2, text="Show Answer", command=self.show_answer
        )
        self.show_answer_button.pack(side=tk.LEFT)

        self.skip_button = tk.Button(self.f2, text="Skip", width=6, command=self.skip)
        self.skip_button.pack(side=tk.LEFT)

        self.thup_button = tk.Button(
            self.f2, text="\U0001f44D", width=5, command=self.thup
        )
        self.thup_button.pack(side=tk.LEFT)

        self.thdn_button = tk.Button(
            self.f2, text="\U0001f44E", width=5, command=self.thdn
        )
        self.thdn_button.pack(side=tk.LEFT)

        self.txt_search = tk.Entry(
            self.frame_options,
            width=65,
            borderwidth=2,
            relief="groove",
        )
        self.txt_search.grid(row=7, column=1, sticky="w", padx=5, pady=1, columnspan=3)

        # setup scrollbar - must use ttk.style for setting the colors
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="lemon chiffon",
            darkcolor="DarkGreen",
            lightcolor="LightGreen",
            troughcolor="gray",
            bordercolor="blue",
            arrowcolor="white",
        )

        self.scrollbar = self.AutoScrollbar(
            self.frame_qa,
            orient="vertical",
            command=self.txt_answer.yview,
        )
        self.scrollbar.grid(row=4, column=9, sticky="nse")
        self.txt_answer["yscrollcommand"] = self.scrollbar.set

        # hide screen by using transparancy mode, center it, then bring it back
        # note: this is a workaround - I found that using withdraw and deiconify didn't work properly on a mac
        master.attributes("-alpha", 0)
        master.update()
        width = master.winfo_width()
        height = master.winfo_height()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        master.geometry("%dx%d+%d+%d" % (width, height, x, y))
        master.attributes("-alpha", 1)
        master.minsize(1200, 710)

        # configure bindings
        self.frame_qa.bind(
            "<Configure>",
            self.rescale,
        )
        self.txt_answer.bind("<MouseWheel>", self.scrollwheel)
        self.txt_search.bind("<Return>", self.callback_search)
        self.txt_search.bind("<FocusIn>", self.callback_sfocus)
        self.bindkeys()

        # start showing the 1st card
        self.rescale(0)
        self.show_card()

    # subclass scrollbar for auto-hide effect
    class AutoScrollbar(ttk.Scrollbar):
        def set(self, low, high):

            if float(low) <= 0.0 and float(high) >= 1.0:
                # Using grid_remove
                self.tk.call("grid", "remove", self)
            else:
                self.grid()

            ttk.Scrollbar.set(self, low, high)

    def callback_peek(self):

        if self.tk_peek.get() == True:
            common.ini["peekmode"] = "True"
        else:
            common.ini["peekmode"] = "False"
        common.save_ini()
        self.show_card()

    def scrollwheel(self, event):
        return "break"

    def rescale(self, event):

        # calculate pixels per character for width
        a = self.txt_answer.winfo_width()
        b = self.txt_answer["width"]
        common.ini["width"] = b
        ppc = a // b

        # calculate how many chars fit in frame
        d = self.frame_qa.winfo_width()
        char_in_frame = d // ppc

        self.txt_answer["width"] = char_in_frame - 20
        self.txt_topic["width"] = char_in_frame - 20
        self.txt_question["width"] = char_in_frame - 20
        self.txt_section["width"] = char_in_frame - 20

        # calculate pixels per character for height
        a = self.txt_answer.winfo_height()
        b = self.txt_answer["height"]
        common.ini["height"] = b
        ppc = a // b

        # update ini
        common.save_ini()

        # calculate how many chars fit in frame
        d = self.frame_qa.winfo_height()
        char_in_frame = d // ppc
        self.txt_answer["height"] = char_in_frame - 12

        return

    def skip(self):
        if common.myFlashcards.getCard(self.currentcard) == {}:
            return

        self.currentcard = common.myFlashcards.toggleSkip(self.currentcard)
        common.save_cache()

        self.show_card()

    def thup(self):
        if common.myFlashcards.getCard(self.currentcard) == {}:
            return

        common.myFlashcards.incThup(self.currentcard)
        common.save_cache()

        if self.tk_autonext.get() == True:
            self.currentcard = common.myFlashcards.next(self.currentcard)

        self.show_card()

    def thdn(self):
        if common.myFlashcards.getCard(self.currentcard) == {}:
            return

        common.myFlashcards.incThdn(self.currentcard)
        common.save_cache()

        if self.tk_autonext.get() == True:
            self.currentcard = common.myFlashcards.next(self.currentcard)

        self.show_card()

    def clear(self):
        if common.myFlashcards.getCard(self.currentcard) == {}:
            return

        # warning
        result = messagebox.showwarning(
            "Title", "Are you sure?", type=messagebox.OKCANCEL, default="cancel"
        )
        if result == "cancel":
            return

        # user pressed ok
        common.clear_cache()
        common.myFlashcards.loadCards()
        self.currentcard = 0
        self.show_card()

    def load_file(self):

        # try to retain the same working directory if we already had an mdfile
        if "/" in common.ini["mdFile"]:
            currdir = common.ini["mdFile"].rsplit("/", 1)[0]
        else:
            currdir = "/"

        # dialog, asking for a new filename
        filename = tk.filedialog.askopenfilename(
            initialdir=currdir,
            title="Select file",
            filetypes=(("md files", "*.md"), ("all files", "*.*")),
        )

        # take back the focus
        self.master.focus_force()

        # do nothing if cancelled
        if not filename:
            return
        else:
            common.ini["mdFile"] = filename

        # reload cards
        common.myFlashcards.loadCards()
        self.currentcard = 0

        # autosave settings
        common.save_ini()

        # load 1st card, reset selection
        self.currentcard = 0
        self.show_card()

    def previous(self):
        self.currentcard = common.myFlashcards.previous(self.currentcard)
        self.show_card()

    def previous_key(self, event):
        self.previous()

    def callback_autonext(self):

        if self.tk_autonext.get() == True:
            common.ini["autonext"] = "True"
        else:
            common.ini["autonext"] = "False"
        common.save_ini()

    def callback_display(self, event):
        common.ini["display"] = self.display_cb.get()
        common.save_ini()
        common.save_cache()
        common.myFlashcards.updateView()
        self.currentcard = 0
        self.show_card()

    def callback_sfocus(self, event):
        self.unbindkeys()

    def callback_search(self, event):
        common.ini["search"] = self.txt_search.get().rstrip("\n")
        common.save_ini()
        self.bindkeys()
        self.show_answer_button.focus_set()
        common.myFlashcards.updateView()
        self.currentcard = 0
        self.show_card()

    def callback_searchfocus(self, event):
        self.txt_search.focus_set()

    def bindkeys(self):
        self.master.bind("<Right>", self.next_key)
        self.master.bind("<Left>", self.previous_key)
        self.master.bind("a", self.show_answer_key)
        self.master.bind("<Return>", self.callback_searchfocus)

    def unbindkeys(self):
        self.master.unbind("<Right>")
        self.master.unbind("<Left>")
        self.master.unbind("a")
        self.master.unbind("<Return>")

    def next(self):
        self.currentcard = common.myFlashcards.next(self.currentcard)
        self.show_card()

    def next_key(self, event):
        self.next()

    def random(self):

        # set current to a randomly picked card
        self.currentcard = random.randint(0, common.myFlashcards.totalView())

        self.currentcard = common.myFlashcards.next(self.currentcard)
        self.show_card()

    def show_answer(self):

        global my_image
        my_image = []
        image_counter = 0

        self.fields_to_normal()
        card = common.myFlashcards.getCard(self.currentcard)

        if card != {}:
            self.txt_answer.delete("1.0", "end")
            self.txt_answer.insert(tk.END, "\n\n")
            for line in card["Answer"]:
                if line.strip().startswith("(image)["):
                    self.txt_answer.insert(tk.END, "\n\t")

                    org_filepath = line.strip()[:-1].split("[")[1]

                    if not os.path.exists(org_filepath):
                        dir_path = os.path.dirname(os.path.realpath(__file__))
                        org_filepath = dir_path + "/" + org_filepath

                    try:
                        my_image.append(PhotoImage(file=org_filepath))
                        self.txt_answer.image_create(
                            tk.INSERT, image=my_image[image_counter]
                        )

                        self.txt_answer.insert(tk.END, "\n\n")
                        image_counter += 1

                    except Exception as err:
                        print(f"Some issues with file {org_filepath}....")
                        print(err)

                else:
                    if line.strip() == "":
                        pline = line
                    else:
                        # insert bullet itself if not opted out for with \*
                        if not line.startswith(" \*"):
                            # insert spaces before the bullet sign if applicable
                            pline = " " * (len(line) - len(line.lstrip()))
                            pline += " \u2022 " + line.lstrip()
                        else:
                            pline = " " * (len(line) - len(line[3:].lstrip()))
                            pline += line[3:].lstrip()

                    self.txt_answer.insert(tk.END, pline)

        self.fields_to_disabled()

    def show_answer_key(self, event):
        self.show_answer()

    def fields_to_normal(self):
        self.txt_topic.configure(state="normal")
        self.txt_section.configure(state="normal")
        self.txt_question.configure(state="normal")
        self.txt_answer.configure(state="normal")
        self.txt_file.configure(state="normal")
        self.txt_totq.configure(state="normal")
        self.txt_skipped.configure(state="normal")
        self.txt_thup.configure(state="normal")
        self.txt_thdn.configure(state="normal")
        self.txt_currq.configure(state="normal")

    def fields_to_disabled(self):
        self.txt_topic.configure(state="disabled")
        self.txt_section.configure(state="disabled")
        self.txt_question.configure(state="disabled")
        self.txt_answer.configure(state="disabled")
        self.txt_file.configure(state="disabled")
        self.txt_totq.configure(state="disabled")
        self.txt_skipped.configure(state="disabled")
        self.txt_thup.configure(state="disabled")
        self.txt_thdn.configure(state="disabled")
        self.txt_currq.configure(state="disabled")

    def show_card(self):

        # make all fields editable (required for updating them)
        self.fields_to_normal()

        # delete current data
        self.txt_topic.delete("1.0", "end")
        self.txt_section.delete("1.0", "end")
        self.txt_question.delete("1.0", "end")
        self.txt_answer.delete("1.0", "end")
        self.txt_skipped.delete("1.0", "end")
        self.txt_currq.delete("1.0", "end")
        self.txt_search.delete(0, "end")
        self.txt_file.delete("1.0", "end")
        self.txt_totq.delete("1.0", "end")
        self.txt_thup.delete("1.0", "end")
        self.txt_thdn.delete("1.0", "end")

        # set autonext to correct value
        if common.ini["autonext"] == "True":
            self.tk_autonext.set(True)
        else:
            self.tk_autonext.set(False)

        # set display mode to correct value
        self.display_cb.current(self.display_cb["values"].index(common.ini["display"]))

        # set search field to saved value
        self.txt_search.insert(0, common.ini["search"])

        # set peekmode to saved value
        if common.ini["peekmode"] == "True":
            self.tk_peek.set(True)
        else:
            self.tk_peek.set(False)

        # handle cases with no valid cards
        if common.myFlashcards.totalCards() == 0:
            self.txt_topic.insert(
                tk.END,
                " No cards in file (try loading a different .md file) ",
            )
            self.fields_to_disabled()
            return

        if common.myFlashcards.totalView() == 0:
            self.txt_topic.insert(
                tk.END,
                " No cards in selection (try showing all cards or search for a different string) ",
            )
            self.fields_to_disabled()
            return

        # get current card info
        card = common.myFlashcards.getCard(self.currentcard)

        # update skip button
        if common.myFlashcards.getTagSkipped(self.currentcard):
            self.skip_button.config(text="Unskip")
        else:
            self.skip_button.config(text=" Skip ")

        # update thup/thdn buttons
        thupnr = common.myFlashcards.getThup(self.currentcard)
        self.thup_button.config(text=f"\U0001f44D : {thupnr}")
        thdnnr = common.myFlashcards.getThdn(self.currentcard)
        self.thdn_button.config(text=f"\U0001f44E : {thdnnr}")

        # put card in subsequent textboxes (do not show answer yet)
        self.txt_topic.insert(tk.END, card["Topic"])
        self.txt_section.insert(tk.END, card["Section"])
        self.txt_question.insert(tk.END, card["Question"].split("(fltags:")[0])

        # filename
        fn = common.ini["mdFile"]
        if len(fn) > 80:
            while len(fn) > 80:
                fn = fn.split("/", 1)[1]
            fn = ".../" + fn
        self.txt_file.insert(tk.END, fn)

        # stats section
        self.txt_totq.insert(
            tk.END,
            str(common.myFlashcards.totalCards()),
        )

        self.txt_skipped.insert(tk.END, common.myFlashcards.totalSkipped())
        self.txt_thup.insert(tk.END, common.myFlashcards.totalwthup())
        self.txt_thdn.insert(tk.END, common.myFlashcards.totalwthdn())

        self.txt_currq.insert(
            tk.END,
            str(self.currentcard + 1) + "/" + str(common.myFlashcards.totalView()),
        )

        # also show answer when in peek mode
        if self.tk_peek.get() == True:
            self.show_answer()

        self.fields_to_disabled()
