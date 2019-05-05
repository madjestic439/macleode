import sqlite3
import time
import os
#import scan

class Base:
    """data manager"""
    def __init__(self):
        """Constructor"""
        self.ext = 'sqlite'
        self.clean_db_zone()
        self.f_base = 'my_base_'+str(time.time())+'.'+self.ext
        self.tb_link = 'tb_links'
        self.tb_link_colomn = ['id_link', 'link', 'size', 'extention']
        self.tb_c = 'tb_correspondance'
        self.tb_c_colomn = ['id_c', 'list_ln', 'nb']
        self.conn = sqlite3.connect(self.f_base)
        self.curs = self.conn.cursor()
        self.nb_doublon = 0

    def creation(self):
        """database creation"""
        print('datatable creation...')
        self.curs.execute("CREATE TABLE IF NOT EXISTS {}({} INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, {} TEXT UNIQUE, {} TEXT, {} TEXT)".format(self.tb_link, self.tb_link_colomn[0], self.tb_link_colomn[1], self.tb_link_colomn[2], self.tb_link_colomn[3]))
        self.curs.execute("CREATE TABLE IF NOT EXISTS {}({} INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, {} TEXT UNIQUE, {} INTEGER)".format(self.tb_c, self.tb_c_colomn[0], self.tb_c_colomn[1], self.tb_c_colomn[2]))
        self.conn.commit()
        print('datatable created')

    def add_link(self, link):
        """add a file(link, size, ext)"""
        try:
            self.curs.execute("INSERT INTO {}({}, {}, {}) VALUES(?, ?, ?)".format(self.tb_link, self.tb_link_colomn[1], self.tb_link_colomn[2], self.tb_link_colomn[3]), link)
        except sqlite3.IntegrityError as e:
            pass

    def suppr_link(self, id):
        """delete a link by id"""
        self.curs.execute("DELETE FROM {} WHERE {} = ?".format(self.tb_link, self.tb_link_colomn[0]), (id,))

    def get_all_link(self):
        """get all files saved"""
        self.curs.execute("SELECT * FROM {} ORDER BY {}, {}".format(self.tb_link, self.tb_link_colomn[3], self.tb_link_colomn[2]))
        return self.curs.fetchall()

    def analyse(self):
        """lance the analyse's programm: detect the same files"""
        print('Analyzing all files...')
        links = self.get_all_link()
        for link in links:
            self.the_one(link)

    def the_one(self, link):
        """get the same files and save it"""
        self.curs.execute("SELECT * FROM {} WHERE {} = '{}' AND {} = '{}' ORDER BY {}".format(self.tb_link, self.tb_link_colomn[2], link[2], self.tb_link_colomn[3], link[3], self.tb_link_colomn[0]))
        data_c = self.curs.fetchall()
        if len(data_c) > 1 :
            str_lst_l = ''
            nb = 0
            for c in data_c :
                if nb > 0 :
                    str_lst_l += ','
                str_lst_l += str(c[0])
                nb += 1
            try:
                self.curs.execute("INSERT INTO {}({}, {}) VALUES(?, ?)".format(self.tb_c, self.tb_c_colomn[1], self.tb_c_colomn[2]), (str_lst_l, nb))
            except sqlite3.IntegrityError as e:
                self.nb_doublon += 1

    def get_all_c(self):
        """get all correspondances"""
        print('reading all correspondances...')
        self.curs.execute("SELECT * FROM {} ORDER BY {}".format(self.tb_c, self.tb_c_colomn[0]))
        return self.curs.fetchall()

    def get_on_c(self, on_c):
        """on correspondance by links id"""
        print('loading on correspondance...')
        self.curs.execute("SELECT * FROM {} WHERE {} IN ({}) ORDER BY {}".format(self.tb_link, self.tb_link_colomn[0], on_c, self.tb_link_colomn[0]))
        return self.curs.fetchall()

    def clean_db_zone(self):
        """renit database"""
        print('deleting datatable...')
        for fl in os.listdir():
            elem = os.path.abspath(fl)
            tab_point = elem.split('.')
            if len(tab_point) > 1 and tab_point[-1] == self.ext:
                os.remove(fl)
        print('datatable deleted')

if __name__ == "__main__":
    all = [('test1', '134', 'ext1'),('test2', '134', 'ext2'),('test1', '134', 'ext1'),('test3', '134', 'ext3'),('test4', '134', 'ext4'),('test1', '134', 'ext1'),('test2', '134', 'ext2'),('test5', '134', 'ext5')]
    base = Base()
    base.creation()
    """scan = scan.Scan('/home/madjestic/')
    scan.execute()
    all = scan.fichiers"""
    for fichier in all:
        base.add_link(fichier)
    links = base.get_all_link()
    for link in links:
        print("{} -> {} => {} , ext: {}".format(link[0], link[1], link[2], link[3]))
