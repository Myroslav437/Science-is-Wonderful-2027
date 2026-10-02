"""Closed multilingual vocabulary: spoken word -> canonical slot value.

Only words in this list can ever reach the robot's representation. That keeps
the system child-safe (no free-text inference) and makes every spoken-word
explanation checkable ("I heard 'chien'"). Languages: EN, FR, NL, DE, PL
(the fair's visitors speak mostly French and Dutch). Matching uses the
language Whisper detected (plus English), so English "chat" is not a French
cat and English "pies" is not a Polish dog.
"""
from __future__ import annotations

import re
import unicodedata

LEXICON = {
    "colour": {
        "red":    {"en": "red", "fr": "rouge rouges", "nl": "rood rode", "de": "rot rote roten", "pl": "czerwony czerwona czerwone"},
        "orange": {"en": "orange", "fr": "orange oranges", "nl": "oranje", "de": "orange orangene", "pl": "pomarańczowy pomarańczowa pomarańczowe"},
        "yellow": {"en": "yellow", "fr": "jaune jaunes", "nl": "geel gele", "de": "gelb gelbe", "pl": "żółty żółta żółte"},
        "green":  {"en": "green", "fr": "vert verte verts vertes", "nl": "groen groene", "de": "grün grüne", "pl": "zielony zielona zielone"},
        "blue":   {"en": "blue", "fr": "bleu bleue bleus bleues", "nl": "blauw blauwe", "de": "blau blaue", "pl": "niebieski niebieska niebieskie granatowy"},
        "purple": {"en": "purple violet", "fr": "violet violette mauve", "nl": "paars paarse", "de": "lila violett", "pl": "fioletowy fioletowa fioletowe"},
        "pink":   {"en": "pink", "fr": "rose roses", "nl": "roze", "de": "rosa pink", "pl": "różowy różowa różowe"},
        "brown":  {"en": "brown", "fr": "marron brun brune", "nl": "bruin bruine", "de": "braun braune", "pl": "brązowy brązowa brązowe"},
        "black":  {"en": "black", "fr": "noir noire noirs", "nl": "zwart zwarte", "de": "schwarz schwarze", "pl": "czarny czarna czarne"},
        "white":  {"en": "white", "fr": "blanc blanche blancs", "nl": "wit witte", "de": "weiß weiss weiße", "pl": "biały biała białe"},
        "grey":   {"en": "grey gray", "fr": "gris grise", "nl": "grijs grijze", "de": "grau graue", "pl": "szary szara szare"},
    },
    "animal": {
        "dog":      {"en": "dog dogs puppy puppies doggy", "fr": "chien chiens chienne chiot", "nl": "hond honden hondje", "de": "hund hunde", "pl": "pies psy piesek psa pieski"},
        "cat":      {"en": "cat cats kitten kitty", "fr": "chat chats chaton", "nl": "kat katten poes poesje", "de": "katze katzen", "pl": "kot koty kotek kota kotki"},
        "horse":    {"en": "horse horses pony ponies", "fr": "cheval chevaux poney", "nl": "paard paarden pony", "de": "pferd pferde pony", "pl": "koń konie konia"},
        "rabbit":   {"en": "rabbit rabbits bunny bunnies", "fr": "lapin lapins", "nl": "konijn konijnen", "de": "hase hasen kaninchen", "pl": "królik króliki królika"},
        "bird":     {"en": "bird birds parrot", "fr": "oiseau oiseaux perroquet", "nl": "vogel vogels papegaai", "de": "vogel vögel papagei", "pl": "ptak ptaki ptaka papuga"},
        "fish":     {"en": "fish fishes", "fr": "poisson poissons", "nl": "vis vissen", "de": "fisch fische", "pl": "ryba ryby rybka"},
        "lion":     {"en": "lion lions", "fr": "lion lions", "nl": "leeuw leeuwen", "de": "löwe löwen", "pl": "lew lwy lwa"},
        "elephant": {"en": "elephant elephants", "fr": "éléphant éléphants", "nl": "olifant olifanten", "de": "elefant elefanten", "pl": "słoń słonie słonia"},
        "bear":     {"en": "bear bears teddy", "fr": "ours nounours", "nl": "beer beren", "de": "bär bären", "pl": "niedźwiedź miś misiu"},
        "monkey":   {"en": "monkey monkeys", "fr": "singe singes", "nl": "aap apen", "de": "affe affen", "pl": "małpa małpy małpka"},
        "turtle":   {"en": "turtle turtles tortoise", "fr": "tortue tortues", "nl": "schildpad schildpadden", "de": "schildkröte schildkröten", "pl": "żółw żółwie żółwia"},
        "dinosaur": {"en": "dinosaur dinosaurs dino", "fr": "dinosaure dinosaures", "nl": "dinosaurus dinosaurussen", "de": "dinosaurier", "pl": "dinozaur dinozaury dinozaura"},
    },
}
LANGS = ("en", "fr", "nl", "de", "pl")


def fold(word: str) -> str:
    w = word.lower().replace("ł", "l").replace("ß", "ss")
    w = unicodedata.normalize("NFKD", w)
    return "".join(c for c in w if not unicodedata.combining(c))


# INDEX[lang][folded word] = (slot, canonical value)
INDEX: dict[str, dict[str, tuple[str, str]]] = {lang: {} for lang in LANGS}
for _slot, _table in LEXICON.items():
    for _canon, _bylang in _table.items():
        for _lang, _words in _bylang.items():
            for _w in _words.split():
                INDEX[_lang][fold(_w)] = (_slot, _canon)


def tokens(text: str) -> list[str]:
    return [t for t in re.split(r"[^\w]+", fold(text)) if t]


def find_keywords(words, language: str | None = None):
    """words: iterable of (word, start, end, prob) from ASR.

    Yields (slot, value, spoken_word, start, prob). Uses the detected
    language's list plus English (children mix languages).
    """
    langs = ["en"] + ([language] if language in INDEX and language != "en" else [])
    if language not in INDEX:
        langs = list(LANGS)  # unknown language: accept all lists
    for w, start, end, prob in words:
        for tok in tokens(w):
            for lang in langs:
                if tok in INDEX[lang]:
                    slot, value = INDEX[lang][tok]
                    yield slot, value, w.strip(), start, prob
                    break
