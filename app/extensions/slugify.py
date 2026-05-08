import unicodedata
import re

class Slugify:
    @staticmethod
    def slugify(texto):
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        texto = texto.lower()
        texto = re.sub(r'[^a-z0-9]+', '-', texto)
        return texto.strip('-')
