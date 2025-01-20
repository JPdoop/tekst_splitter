import pyphen
import re
import streamlit as st

# Initialiseer Pyphen
dic = pyphen.Pyphen(lang='nl_NL')

# Titel van de webapp
st.title("Lettergrepen Splitsen met Correcte Markering")

# Introductietekst
st.write(
    "Dag collega's van leersteuncentrum type 7, plak hier de tekst die je in lettergrepen wil zien."
)

# Invoerveld voor de gebruiker
text = st.text_area(
    "Voer je tekst in:", 
    "Dag collega's van leersteuncentrum type 7, plak hier de tekst die je in lettergrepen wil zien."
)

# Lijst met tweeklanken
tweeklanken = [
    "aa", "ae", "ai", "ee", "ey", "eu", "ie", "oe", "oo", "ou", "uu",
    "aai", "aau", "eeu", "ieu", "oei", "ooi", "ui"
]

# Lijst met korte woorden en voorvoegsels die niet gemarkeerd mogen worden
uitzonderingen = {
    "de", "me", "je", "ge", "ze",  # Korte woorden
}
voorvoegsels_met_hoofdletter = {"Ge", "Be", "Ver"}  # Voorvoegsels met hoofdletters

# Functie om open klinkers te markeren
def mark_open_vowels(word):
    # Controleer of het woord in de uitzonderingen valt
    if word.lower() in uitzonderingen:
        return word  # Geen markering

    # Controleer of het woord met een voorvoegsel begint
    if any(word.startswith(prefix) for prefix in voorvoegsels_met_hoofdletter):
        # Splits het woord zonder de voorvoegsel-klinker te markeren
        syllables = dic.inserted(word).split("-")
        marked_syllables = []

        for i, syllable in enumerate(syllables):
            # Markeer alleen als het niet het voorvoegsel is
            if i == 0:  # Eerste lettergreep (voorvoegsel)
                marked_syllables.append(syllable)
            elif len(syllable) > 1 and syllable[-1] in "aeiou":
                # Controleer op tweeklanken
                if not any(tweeklank in syllable for tweeklank in tweeklanken):
                    syllable = re.sub(
                        r"([aeiou])$",  # Zoek de laatste klinker
                        r"<span style='color: red; font-size: 24px;'>\1</span>", 
                        syllable
                    )
                marked_syllables.append(syllable)
            else:
                marked_syllables.append(syllable)
        return "-".join(marked_syllables)

    # Splits het woord normaal in lettergrepen
    syllables = dic.inserted(word).split("-")
    marked_syllables = []

    for i, syllable in enumerate(syllables):
        # Controleer of het woord eindigt op 'e' (geen markering)
        if i == len(syllables) - 1 and word[-1].lower() == "e":
            marked_syllables.append(syllable)
            continue

        # Controleer of het een open klinker is
        if len(syllable) > 1 and syllable[-1] in "aeiou":
            # Controleer op tweeklanken
            if not any(tweeklank in syllable for tweeklank in tweeklanken):
                # Markeer alleen de klinker, niet de hele lettergreep
                syllable = re.sub(
                    r"([aeiou])$",  # Zoek de laatste klinker
                    r"<span style='color: red; font-size: 24px;'>\1</span>", 
                    syllable
                )
        marked_syllables.append(syllable)

    return "-".join(marked_syllables)

# Knop om de tekst te verwerken
if st.button("Splits in lettergrepen"):
    # Gebruik regex om woorden en interpunctie te scheiden
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)

    # Splits woorden en behoud interpunctie
    splitted_tokens = [
        mark_open_vowels(token) if token.isalpha() or token.replace("'", "").isalpha() else token
        for token in tokens
    ]

    # Combineer tokens terug tot een tekst met 3 spaties tussen woorden
    splitted_text = '   '.join(
        [token if re.match(r"[^\w\s]", token) else f"{token}" for token in splitted_tokens]
    ).strip()

    # Toon de gesplitste tekst in lettergrepen met gemarkeerde klinkers
    st.markdown(f"<div style='font-size: 18px;'>{splitted_text}</div>", unsafe_allow_html=True)
