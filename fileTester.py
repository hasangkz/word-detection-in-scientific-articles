from tika import parser  # pip install tika
import numpy as np # pip install numpy


class WordClass():
    BAN_WORDS = ['into', 'back', "when", "that", "with", "very", "also"]

    def __init__(self, filename: str):
        self.filename = filename
        self.words = set()

        # kelimeleri yukle
        self.InitWords()

    def InitWords(self):
        print("Dosya okunuyor..")
        words = self.ReadFile()
        print("%d kelime filtreleniyor.." % len(words))
        self.FilterWords(words)
        print("Islemler tamamlandi. Kelime sayisi = %d" % len(self.words))

    # override edilecek
    def ReadFile(self) -> list:
        return ""

    # kelimelerin diger bir kelimelerle olan benzerligini bul
    def GetSimilarity(self, other_word_class: object) -> float:
        # ortak kelimelerin uzunlugnu bul
        intersection = len(
            list(self.words.intersection(other_word_class.words)))
        # toplam kelime sayisindan ortaklari cikart, uyumsuz olan toplam kelime sayisini bul
        union = (len(self.words) + len(other_word_class.words)) - intersection
        # ortak sayi / ortak olmayanlar seklinde float bir deger dondur
        return float(intersection) / union

    # gelen wordleri filtreleyip self.words setine at
    def FilterWords(self, words: list):
        # self.words = [ val.lower() for val in words if val.isalpha() and len(val) > 3 and val.lower() not in self.BAN_WORDS ]
        # gelen her kelime icin
        for val in words:
            # kelimedeki sadece harf olanlari kucuk harfe cevirerek al
            val = ''.join([i.lower() for i in val if i.isalpha()])
            # kisa ve gereksiz sozcuklerden biri degilse
            if len(val) > 3 and val not in self.BAN_WORDS:
                # sete ekle
                self.words.add(val)

# text dosyalarinda normal sekilde okuyacagiz ve split edip kelimelere ayiracagiz


class TextFile(WordClass):
    def ReadFile(self):
        with open(self.filename, 'r') as file:
            return file.read().split()

# pdf dosyalarinda kutuphane kullanarak okuyacagiz ve icerigi split edip kelimelerine ayiracagiz


class PDFFile(WordClass):
    def ReadFile(self):
        content = parser.from_file(self.filename)['content']
        return content.split()

# alanlarin ismi ve txt dosyalari tipinden attributeleri olacak


class Alan():  # bolum anlaminda
    def __init__(self, name: str, textFileName: str):
        self.name = name
        self.textFile = TextFile(textFileName)

# benzerlik bulunurken pdf dosyasini ve alanlari verecegiz


class Similarty():
    def __init__(self, pdfFile: PDFFile, alanlar: list):
        self.pdfFile = pdfFile
        self.alanlar = alanlar

    # pdf in en yakin oldugu alanin indexini dondurecegiz
    def FindBestSimilarty(self):
        # benzerlik oranlarini tutmak icin liste olusturuyoruz
        self.benzerlikOranlari = []
        # her bir alan icin
        for alan in self.alanlar:
            # alanlariin pdf belgesine olan benzerligini bulup listeye atiyoruz
            self.benzerlikOranlari.append(
                self.pdfFile.GetSimilarity(alan.textFile))
        # listedeki en buyuk benzerlik oranina sahip verinin indexini donduruyoruz
        return np.argmax(self.benzerlikOranlari)


# alanlari olusturuyoruz
alanlar = [Alan('tarih', 'texts/hs_text.txt'), Alan('tip',
                                                    'texts/md_text.txt'), Alan('matematik', 'texts/mt_text.txt')]

# pdfleri olusturuyoruz
pdfler = [
    PDFFile('dataset/matematik/a-theorem-on-inverses-of-tridiagonal-matrices.pdf'),
    PDFFile('dataset/matematik/norm-estimates-for-inverses-of-vandermonde-matrices.pdf'),
    PDFFile('dataset/matematik/positive-definite-matrices-and-the-s-divergence.pdf'),

    PDFFile('dataset/tarih/history-of-us-vol-x-ch1.pdf'),
    PDFFile('dataset/tarih/the-british-empire-city-states-and-commercially-oriented-politics.pdf'),
    PDFFile('dataset/tarih/the-ottoman-empire-and-the-capitalist-world-economy.pdf'),

    PDFFile('dataset/tip/advances-in-gene-therapy-technologies.pdf'),
    PDFFile('dataset/tip/age-related-macular-degeneration.pdf'),
    PDFFile('dataset/tip/patients-with-suspected-glaucoma.pdf'),
]

# her bir pdf icin
for pdf in pdfler:
    # benzerlik nesnesi olusturuyoruz
    benzerlik = Similarty(pdf, alanlar)
    # en benzer olanin indexini aliyoruz
    maxIndex = benzerlik.FindBestSimilarty()
    # pdf ismini ve en benzer oldugu alanin ismini ekrana yazdiriyoruz
    print(pdf.filename, "  --  ", alanlar[maxIndex].name)
    # print(pdf.filename, "  --  ", benzerlik.benzerlikOranlari, alanlar[maxIndex].name)
