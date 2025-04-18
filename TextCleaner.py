import re
from nltk.stem import WordNetLemmatizer
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize


contraction_mapping = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not",

                           "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not",

                           "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",

                           "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would",

                           "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",

                           "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam",

                           "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have",

                           "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock",

                           "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",

                           "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is",

                           "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as",

                           "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would",

                           "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have",

                           "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have",

                           "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",

                           "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",

                           "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is",

                           "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",

                           "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have",

                           "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all",

                           "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",

                           "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",

                           "you're": "you are", "you've": "you have"}

stop_words = set(stopwords.words('english')) 
nltk.download('wordnet', quiet=True)
nlp = spacy.load("en_core_web_sm")
url_pattern = re.compile(r'https?://\S+|www\.\S+')
html_pattern = r'<.*?>'

lemmatizer = WordNetLemmatizer()

def lower_text(text):
    split_text = text.split(' ')
    for i in range(len(split_text)):
        if not split_text[i].isupper() or len(split_text[i]) == 1:
            split_text[i] = split_text[i].lower()
    return " ".join(split_text)

def lemmanize_text(tokens):
    lemmatized_tokens = []
    for w in tokens:
        if w.isupper():
            lemmatized_tokens.append(w)
        else:
            lemmatized_tokens.append(lemmatizer.lemmatize(w))
    
    return lemmatized_tokens        

"""
Cleans the text of unnecessary parts such as uppercase leeters, unncesssary spaces, urls, htmls, clsoed paranthesis, quotations,
contradictions, punctuations and special characters, stopwords, and short words
"""
def clean_text(tokenized_text):
    for i in range(len(tokenized_text)):
        new_token = lower_text(tokenized_text[i])
        new_token = re.sub(" +", ' ', new_token)
        new_token = url_pattern.sub(r'', new_token)
        new_token = re.sub(html_pattern, '', new_token)
        new_token = re.sub(r'\([^)]*\)', '', new_token)
        new_token = re.sub('"','', new_token)
        new_token = ' '.join([contraction_mapping[t] if t in contraction_mapping else t for t in new_token.split(" ")])    
        new_token = re.sub(r"'s\b","",new_token)
        new_token = re.sub("&", "", new_token)
        new_token = re.sub("[^a-zA-Z0-9%.]", " ", new_token)
        doc = nlp(new_token)
        filtered_tokens = []
        for token in doc:
            if not token.is_stop or token.ent_type_ or token.pos_ == "NUM" or (token.text.replace('.','',1).isdigit() and ('.' in token.text)) or token.text.isdigit() or token.text == "%":
                filtered_tokens.append(token.text)
        if filtered_tokens and filtered_tokens[-1] == ".": 
            filtered_tokens.pop() 

        lemmatized_tokens = lemmanize_text(filtered_tokens)
        token = " ".join(lemmatized_tokens)
        token = re.sub(" +", " ", token) 
        token = token.lstrip()
        tokenized_text[i] = token
    
    return tokenized_text
