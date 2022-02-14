
from .models import Cerita, Gambar

def ambil(author):
    gambar  = Gambar.objects.get(author=author)
    cerita = Cerita.objects.filter(author=author)
    for i in cerita:
        gambar.cerita_set.add(i)
    
 