from textblob import TextBlob
from symspellpy.symspellpy import SymSpell, Verbosity
import os
import re

# Load SymSpell only once
sym_spell = SymSpell(max_dictionary_edit_distance=2)
dictionary_path = os.path.join("symspell", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, 0, 1)

def correct_with_textblob(text):
    blob = TextBlob(text)
    corrected = str(blob.correct())
    return highlight_changes(text, corrected)

def correct_with_symspell(text):
    corrected_words = []
    for word in text.split():
        suggestion = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        if suggestion:
            corrected = suggestion[0].term
            if corrected.lower() != word.lower():
                corrected_words.append(f"<mark>{corrected}</mark>")
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
    return " ".join(corrected_words)

def highlight_changes(original, corrected):
    original_words = original.split()
    corrected_words = corrected.split()
    result = []
    for o, c in zip(original_words, corrected_words):
        if o != c:
            result.append(f"<mark>{c}</mark>")
        else:
            result.append(c)
    result.extend(corrected_words[len(original_words):])  # handle extra words
    return " ".join(result)
