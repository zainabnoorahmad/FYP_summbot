import nltk
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import yake

stop_words = set(stopwords.words('english'))

def remove_stopwords(query_tokens):
  stop_words = set(stopwords.words('english'))
  tokens_without_stopwords = []
  for w in query_tokens: 
    if w not in stop_words: 
        tokens_without_stopwords.append(w)
  return tokens_without_stopwords

def lemmetizer(tokens_without_stopwords):
   lemmatized_words = []
   wordnet_lemmatizer = WordNetLemmatizer()
   for w in tokens_without_stopwords:
    word1 = wordnet_lemmatizer.lemmatize(w, pos = "n")
    word2 = wordnet_lemmatizer.lemmatize(word1, pos = "v")
    word3 = wordnet_lemmatizer.lemmatize(word2, pos = ("a"))
    lemmatized_words.append(word3) 
   return lemmatized_words

def unique_words(lemmatized_words):
  uniqueWords = [] 
  for i in lemmatized_words:
      if not i in uniqueWords:
          uniqueWords.append(i)
  return uniqueWords

def join_unique_words(unique_words):
  unique_word_string = " ".join(unique_words)
  return unique_word_string 

def keyword_extract(query):
  keyword_array=[]
  language = "en"
  max_ngram_size = 1
  deduplication_threshold = 0.9 
  numOfKeywords = 20
  custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
  keywords = custom_kw_extractor.extract_keywords(query)
  for kw in keywords:
    keyword_array.append(kw[0])
    return keyword_array


def query_processing(Query):
  Tokens = word_tokenize(Query)
  Keywords= keyword_extract(Query)
  tokens_without_stopwords=remove_stopwords(Tokens)
  lemmatized_tokens = lemmetizer(tokens_without_stopwords)
  unique_words_ = unique_words(lemmatized_tokens)
  processed_query = ' '.join(unique_words_)
  return  processed_query,Keywords

