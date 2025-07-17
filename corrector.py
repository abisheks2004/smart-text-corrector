import re
import os
from textblob import TextBlob
from symspellpy.symspellpy import SymSpell, Verbosity

sym_spell = SymSpell(max_dictionary_edit_distance=2)
dictionary_path = os.path.join("symspell", "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, 0, 1)

def smart_tokenize(text):
    return re.findall(r"[A-Za-z]+|[0-9]+|[^\w\s]", text)

def correct_with_symspell(text):
    wrong_to_correct = []
    output_tokens = []
    for token in smart_tokenize(text):
        if token.isalpha():
            suggestions = sym_spell.lookup(token, Verbosity.CLOSEST, max_edit_distance=2)
            if suggestions:
                corrected = suggestions[0].term
                if corrected.lower() != token.lower():
                    wrong_to_correct.append(f"{token} → {corrected}")
                    output_tokens.append(f"<mark>{corrected}</mark>")
                else:
                    output_tokens.append(token)
            else:
                output_tokens.append(f"<span style='text-decoration: wavy underline red;'>{token}</span>")
        elif token.isdigit():
            output_tokens.append(f"<span style='text-decoration: wavy underline red;'>{token}</span>")
        else:
            output_tokens.append(token)

    formatted_text = ""
    for i, t in enumerate(output_tokens):
        if i > 0 and not re.match(r"[^\w\s]", t):
            formatted_text += " "
        formatted_text += t

    summary = "<br>".join(wrong_to_correct) if wrong_to_correct else "No valid corrections ✅"
    return formatted_text, summary

def correct_with_textblob(text):
    blob = TextBlob(text)
    corrected_text = str(blob.correct())
    orig_words = text.split()
    corr_words = corrected_text.split()
    wrong_to_correct = []
    highlighted_output = []
    for o, c in zip(orig_words, corr_words):
        if o != c:
            wrong_to_correct.append(f"{o} → {c}")
            highlighted_output.append(f"<mark>{c}</mark>")
        else:
            highlighted_output.append(c)
    highlighted_output.extend(corr_words[len(orig_words):])
    formatted = " ".join(highlighted_output)
    summary = "<br>".join(wrong_to_correct) if wrong_to_correct else "No corrections ✅"
    return formatted, summary
