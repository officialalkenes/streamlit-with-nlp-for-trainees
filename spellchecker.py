import streamlit as st
from spellchecker import SpellChecker
import spacy

# Load NLP model
nlp = spacy.load('en_core_web_sm')
spell = SpellChecker()

def check_spelling(text):
    words = text.split()
    misspelled = spell.unknown(words)
    corrections = {word: spell.candidates(word) for word in misspelled}
    return corrections

def check_grammar(text):
    doc = nlp(text)
    grammar_issues = []
    # Example check: Finding repeated phrases
    for sent in doc.sents:
        last_token = ""
        for token in sent:
            if token.text == last_token:
                grammar_issues.append(f"Repeated word: {token.text}")
            last_token = token.text
    return grammar_issues

def main():
    st.title('Grammar and Spell Checker')
    text = st.text_area("Enter Text:", value='', height=200)
    if st.button('Check Text'):
        spelling_corrections = check_spelling(text)
        grammar_issues = check_grammar(text)
        
        if spelling_corrections:
            st.subheader('Spelling Corrections Suggested:')
            for word, corrections in spelling_corrections.items():
                st.write(f"{word}: {list(corrections)}")
        else:
            st.write("No spelling mistakes found!")
        
        if grammar_issues:
            st.subheader('Grammar Issues:')
            for issue in grammar_issues:
                st.write(issue)
        else:
            st.write("No grammar issues found!")

if __name__ == '__main__':
    main()
