import composit_class.scan
import composit_class.base
import os

class Moteur:
    """the moteur"""

    def __init__(self):
        self.base = composit_class.base.Base()
        self.zones = []
        self.urls = []
        self.all_c = []
        self.nb_f = 0
        self.nb_c = 0
        self.current_c = 0
        self.nb_suppr = 0

    def add_zone(self, zone):
        """add repository"""
        zone = str(zone).strip()
        if zone not in self.urls:
            scan = composit_class.scan.Scan(zone)
            if(scan.is_valid_zone()):
                self.zones.append([scan, zone, 0])
                self.urls.append(zone)
                return (True, '')
            else:
                return (False, 'Invalide URL')
        else:
            return (False, 'URL doublon')

    def del_zone(self, zone):
        """delete repository"""
        zone = zone.strip()
        ln = 0
        for scan in self.urls:
            if zone == scan:
                self.urls.pop(ln)
                self.zones.pop(ln)
                return True
            ln += 1
        return False

    def go(self):
        """run scan and analyse"""
        self.base.creation()
        for scan in self.zones:
            scan[0].execute()
            for fichier in scan[0].fichiers:
                self.base.add_link(fichier)
                self.nb_f += 1
        self.base.analyse()
        self.all_c = self.base.get_all_c()
        self.nb_c = len(self.all_c)

    def get_next_c(self):
        """get correspondance"""
        if self.current_c >= self.nb_c :
            return None
        current_line_c = self.all_c[self.current_c]
        self.current_c += 1
        return self.base.get_on_c(current_line_c[1])
    
    def not_last(self):
        return self.current_c <= self.nb_c-1

    def suppr_links(self, link):
        """delete links"""
        rm = True
        try:
            os.remove(link)
        except Exception as e:
            print(str(e))
            rm = False
            return False
        if rm :
            self.nb_suppr += 1
            return True
