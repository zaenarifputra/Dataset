from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

stop_factory = StopWordRemoverFactory()
stop_remover = stop_factory.create_stop_word_remover()
stopwords = set(stop_factory.get_stop_words())

stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

def cleanse(text):
    print(f"\n🧹 Input asli: {text}")
    text = text.lower()
    print(f"🔻 Lowercase: {text}")
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    print(f"🔻 Hapus simbol & angka: {text}")

    # Stopword removal manual untuk melihat yang dihapus
    words = text.split()
    removed = [word for word in words if word in stopwords]
    remaining = [word for word in words if word not in stopwords]
    print(f"🛑 Stopwords dihapus: {removed}")
    print(f"✅ Teks tanpa stopwords: {' '.join(remaining)}")

    text = " ".join(remaining)
    stemmed = stemmer.stem(text)
    print(f"🌱 Setelah stemming: {stemmed}")
    return stemmed
