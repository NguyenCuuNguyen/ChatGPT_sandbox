import spacy
import csv
import re
import html
import itertools
import pandas as pd
from autocorrect import Speller
from spacy.lang.en.stop_words import STOP_WORDS #TODO: account for any other language
from spacy.lang.ja.stop_words import STOP_WORDS 

#BaseEstimator, TransformerMixin
class CleanText():
    """
    Class for preprocessing
    the text documents
    """
        
    def __init__(self, language):
        self.language = language
        if language == 'en':
            self.nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
            self.stop_words = self.nlp.Defaults.stop_words
            self.stop_words -= {'no','nâ€˜t','not','nothing', "n't", 'nor'}
            self.spell = Speller(lang='en')
        elif language == 'fr':
            self.nlp = spacy.load('fr_core_news_sm', disable=['parser', 'ner'])
            self.stop_words = self.nlp.Defaults.stop_words
            self.stop_words -= {u"n",u"n'",u'nâ€˜t',u'na',u'ne', u"n't", u'nul', u"n’", u'non'}
            self.spell = Speller(lang='fr')
        elif language == 'ja':
            self.nlp = spacy.load("ja_core_news_sm")
            self.stop_words = pd.read_table('http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt', header=None)
            self.stop_words = set(self.stop_words[0].values)
            self.stop_words = self.stop_words.union({u'なる',u'いる',u'する',u'れる',u'下さる',u'いく',u'ある',u'おる',u'られる',u'いただく',u'くださる',u'参る',u'せる',u'くる',u'まいる',u'いたす'})
            self.stop_words = self.stop_words.union(STOP_WORDS)

    def remove_mentions(self, text):
        return re.sub(r'[@＠]\w+', ' ', text)

    def remove_urls(self, text):
        return re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)

    def remove_hash(self, text):
        return re.sub(r'#([^\s]+)', r'\1', text)

    def manage_html(self, text):
        return html.unescape(text)

    def remove_newline(self, text):
        return re.sub('\n+', ' ', text)

    def spelling(self, text):
        text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
        words = text.split()
        words = [self.spell(word) for word in words]
        return ' '.join(words)

    def emoji_oneword(self, text):
        # By compressing the underscore, the emoji is kept as one word
        return text.replace('_',' ')

    def to_lower(self, text):
        return text.lower()

    def remove_stopwords(self, text):
        words = text.split()
        words = [word for word in words if not word in self.stop_words]
        return ' '.join(words)
    
    def cleaning(self, text):
        if self.language == 'en':
            text = re.sub(r'[^a-zA-Z!"&\'(),./:;?[]{} ]', ' ', text)
            return text
        elif self.language == 'fr':
            text = re.sub(r'[^a-zA-Z ãàâäèéêëîïôœùûüÿçÀÂÄÈÉÊËÎÏÔŒÙÛÜŸÇ!"&\'()*+,-./:;?[\\]`{|}~«»… ]', ' ', text)
            return text
        elif self.language == 'ja':
            text = re.sub('[^\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A!()（）「」『 』、!！\[\]{};:+\'"\,<>./?-〽。^&*_~Â。…・，【】？]+', ' ', text)
            return text

        else:
            doc = self.nlp(text)
            words = []
            for token in doc:
                word = token.lemma_
                pos = token.pos_
                if pos in ['VERB', 'NOUN', 'ADV', 'ADJ'] and token.text not in self.stop_words:
                    words.append(word)
            return ' '.join(words)


    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        if self.language == 'en':
            clean_text = X.apply(self.manage_html).apply(
            self.to_lower).apply(self.remove_mentions).apply(
            self.remove_urls).apply(self.emoji_oneword).apply(
            self.remove_hash).apply(self.remove_newline).apply(
            self.cleaning).apply(self.remove_stopwords)

        elif self.language == 'fr':
            clean_text = X.apply(self.manage_html).apply(
            self.to_lower).apply(self.remove_mentions).apply(
            self.remove_urls).apply(self.emoji_oneword).apply(
            self.remove_hash).apply(self.remove_newline).apply(
            self.cleaning).apply(self.remove_stopwords).apply(
                self.spelling)

        elif self.language == 'ja':
            clean_text = X.apply(self.manage_html).apply(
            self.to_lower).apply(self.remove_mentions).apply(
            self.remove_urls).apply(self.emoji_oneword).apply(
            self.remove_hash).apply(self.remove_newline).apply(
            self.cleaning).apply(self.normalize)

        return clean_text




def remove_mentions(self, text):
    return re.sub(r'[@＠]\w+', ' ', text)

def remove_urls(self, text):
    return re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)

def remove_hash(self, text):
    return re.sub(r'#([^\s]+)', r'\1', text)

def manage_html(self, text):
    return html.unescape(text)

def remove_newline(self, text):
    return re.sub('\n+', ' ', text)

def spelling(self, text):
    text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
    words = text.split()
    words = [self.spell(word) for word in words]
    return ' '.join(words)

def emoji_oneword(self, text):
    # By compressing the underscore, the emoji is kept as one word
    return text.replace('_',' ')

def to_lower(self, text):
    return text.lower()

def remove_stopwords(self, text):
    words = text.split()
    words = [word for word in words if not word in self.stop_words]
    return ' '.join(words)

def cleaning(self, text):
    if self.language == 'en':
        text = re.sub(r'[^a-zA-Z!"&\'(),./:;?[]{} ]', ' ', text)
        return text
    elif self.language == 'fr':
        text = re.sub(r'[^a-zA-Z ãàâäèéêëîïôœùûüÿçÀÂÄÈÉÊËÎÏÔŒÙÛÜŸÇ!"&\'()*+,-./:;?[\\]`{|}~«»… ]', ' ', text)
        return text
    elif self.language == 'ja':
        text = re.sub('[^\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A!()（）「」『 』、!！\[\]{};:+\'"\,<>./?-〽。^&*_~Â。…・，【】？]+', ' ', text)
        return text

def clean(raw_text_dir):
    # files = [r"C:\Users\Iris Nguyen\Documents\ChatGPT\Data\Colombia - posts.xlsx", r"C:\Users\Iris Nguyen\Documents\ChatGPT\Data\HPV 3k for use case.xlsx", r"C:\Users\Iris Nguyen\Documents\ChatGPT\Data\ML_output_scrambled.csv"]
    
    for file in raw_text_dir:
        ext = file.split('\\')[-1].split('.')[-1]
        with open(file, "rb") as f: 
            if ext == "xlsx":
                df = pd.read_excel(f)
            elif ext == "csv":
                df = pd.read_csv(f)
            df.columns = map(str.lower, df.columns)
            print(df.head(3))
        #txtclean = CleanText('en')
        content = [col for col in df.columns if 'content' in col]
        print(f"content is {content}")
        for con in content:
            print(type(df[con].str))
            df[con] = df[con].replace({r'[@＠]\w+': ' '})
            print(df[con])
            #txt = txtclean.remove_mentions(df[con].str)
            

if __name__ == '__clean__':
    #r"C:\Users\Iris Nguyen\Documents\ChatGPT\Data\Colombia - posts.xlsx", r"C:\Users\Iris Nguyen\Documents\ChatGPT\Data\HPV 3k for use case.xlsx", r"C:\Users\Iris Nguyen\Documents\ChatGPT\Data\ML_output_scrambled.csv"
    clean()


