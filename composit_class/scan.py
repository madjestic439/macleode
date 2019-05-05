import os

class Scan:
    """repertory scanner"""

    def __init__(self, link):
        """constructor"""
        self.link = link
        self.fichiers = []

    def is_valid_zone(self):
        """valide a zone"""
        return os.path.isdir(self.link) and os.path.exists(self.link)

    def execute(self):
        """lancement du scan"""
        print('Scanning "'+self.link+'"...')
        if self.is_valid_zone():
            # = len(self.link) - 1
            if self.link[-1] != '/' :
                self.link += '/'
            try:
                for element in os.listdir(self.link):
                    fichier_element = self.link + element
                    if os.path.islink(fichier_element):
                        continue
                    if os.path.isdir(fichier_element):
                        rep = Scan(fichier_element)
                        rep.execute()
                        fichiers = rep.fichiers
                        for fichier in fichiers:
                            self.fichiers.append(fichier)
                    else:
                        tab_point = element.split('.')
                        extention = ''
                        if len(tab_point) > 1 :
                            extention = tab_point[-1]
                        self.fichiers.append( ( fichier_element, str(os.path.getsize(fichier_element)), extention) )
            except PermissionError as e:
                pass

if __name__ == "__main__":
    scan = Scan('/home/madjestic/Musique')
    scan.execute()
    for fichier in scan.fichiers:
        print('->{}'.format(fichier))
