#!/usr/bin/python3

"""the main prog"""

from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *

import composit_class.moteur

class Ihm:

    def __init__(self):
        self.my_moteur = composit_class.moteur.Moteur()
        self.creat_ihm()
        self.current_crp=[]
    
    def creat_ihm(self):
        self.main_fen = Tk()
        self.main_fen.title('Macleod')
        #self.main_fen.geometry("500x500+10+10")
        #self.main_fen.minsize(510, 510)
        self.main_pan = PanedWindow(self.main_fen, orient=VERTICAL);
        self.main_pan.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
        self.fr_input = LabelFrame(self.main_pan, relief='groove', borderwidth=5, text='Input')
        self.fr_input_bts = Frame(self.fr_input, borderwidth=0, relief='groove', width=30)
        self.bt_select_dir = Button(self.fr_input_bts, text='Add a directory...', command=self.select_dir)
        self.bt_select_dir.pack(side="top", fill="x", pady=5, padx=10)
        self.bt_del_url = Button(self.fr_input_bts, text='Delete', command=self.del_url, state=DISABLED)
        self.bt_del_url.pack(side="top", fill="x", pady=5, padx=10)
        self.fr_input_lst = Frame(self.fr_input, borderwidth=2, relief='groove')
        self.list_url = Listbox(self.fr_input_lst, width=100)
        self.list_url.pack(side="top", fill="both")
        self.fr_input_bts.pack(side='left', fill='both')
        self.fr_input_lst.pack(side='right', fill='both')
        #self.fr_input.pack(side="top", padx=10, pady=10, fill="x")
        self.fr_input.pack(fill='both', anchor=CENTER)
        self.bt_go = Button(self.main_pan, text='Analyze...', command=self.go, state=DISABLED)
        self.bt_go.pack(side="top", pady=5, padx=10, fill='both')
        self.fr_output = LabelFrame(self.main_pan, relief='groove', borderwidth=5, text='Output')
        self.fr_output_bts = Frame(self.fr_output, borderwidth=0, relief='groove', width=30)
        self.bt_del_file = Button(self.fr_output_bts, text='Delete file', command=self.del_file, state=DISABLED)
        self.bt_del_file.pack(side="top", fill="x", pady=5, padx=10)
        self.bt_next = Button(self.fr_output_bts, text='Next', command=self.next, state=DISABLED)
        self.bt_next.pack(side="top", fill="x", pady=5, padx=10)
        self.lbl_nb_file = Label(self.fr_output_bts, text='')
        self.lbl_nb_file.pack(side="top", fill="x", pady=5, padx=10)
        self.lbl_nb_crp = Label(self.fr_output_bts, text='')
        self.lbl_nb_crp.pack(side="top", fill="x", pady=5, padx=10)
        self.lbl_nb_file_del = Label(self.fr_output_bts, text='')
        self.lbl_nb_file_del.pack(side="top", fill="x", pady=5, padx=10)
        self.fr_output_bts.pack(side='left', fill='both')
        self.fr_output_lst = Frame(self.fr_output, borderwidth=2, relief='groove')
        self.list_crp = Listbox(self.fr_output_lst, width=100)
        self.list_crp.pack(side="top", fill="both")
        self.fr_output_lst.pack(side='right', fill='both')
        self.fr_output.pack(fill='both', anchor=CENTER)
        self.main_pan.pack()


    def select_dir(self):
        zone = filedialog.askdirectory(title='directory to analys')
        rep_add_zone=self.my_moteur.add_zone(zone)
        if len(self.my_moteur.zones):
            self.update_list_url()

    def del_url(self):
        index = self.list_url.curselection()
        if len(index):
            zone = self.list_url.get(index[0])
            self.my_moteur.del_zone(zone)
        self.update_list_url()

    def update_list_url(self):
        self.list_url.delete(0, self.list_url.size())
        for url in self.my_moteur.urls:
            self.list_url.insert(self.list_url.size(), url)
        self.bt_del_url.config(state=DISABLED)
        self.bt_go.config(state=DISABLED)
        self.lbl_nb_file.config(text='')
        self.lbl_nb_crp.config(text='')
        if self.list_url.size() :
            self.list_url.select_set(0)
            self.bt_del_url.config(state=NORMAL)
            self.bt_go.config(state=NORMAL)

    def go(self):
        self.bt_go.config(state=DISABLED)
        self.bt_del_url.config(state=DISABLED)
        self.bt_select_dir.config(state=DISABLED)
        self.my_moteur.go()
        self.lbl_nb_file.config(text="Scanned files: {}".format(self.my_moteur.nb_f))
        if self.my_moteur.nb_c:
            self.next()
        else:
            showinfo('Result', 'No duplicated file.')

    def next(self):
        self.current_crp = []
        self.current_crp = self.my_moteur.get_next_c()
        self.update_list_crp()

    def update_list_crp(self):
        self.list_crp.delete(0, self.list_crp.size())
        for crp in self.current_crp:
            self.list_crp.insert(self.list_crp.size(), crp[1])
        self.bt_del_file.config(state=DISABLED)
        if self.list_crp.size():
            self.list_crp.select_set(0)
            self.bt_del_file.config(state=NORMAL)
        self.bt_next.config(state=DISABLED)
        if self.my_moteur.not_last():
            self.bt_next.config(state=NORMAL)
        self.lbl_nb_crp.config(text="duplicated files: {} / {}".format(self.my_moteur.current_c, self.my_moteur.nb_c))
        self.lbl_nb_file_del.config(text="Deleted files: {}".format(self.my_moteur.nb_suppr))

    def del_file(self):
        index = self.list_crp.curselection()
        if len(index):
            file_crp = self.list_crp.get(index[0])
            if askyesno('Delete', file_crp):
                if self.my_moteur.suppr_links(file_crp):
                    #showinfo('Delete', 'file deleted.')
                    self.current_crp.pop(index[0])
                else:
                    showerror("Delete", "Error: file not deleted!")
            self.update_list_crp()
        else:
            showwarning('Delete', 'No file to delete.')

    def run(self):
        self.main_fen.mainloop()

app = Ihm()
app.run()    