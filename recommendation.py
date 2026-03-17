import pandas as pd
import numpy as np

data = pd.read_csv("data/movies.csv")
final_data = data[['title','description']].copy()

import nltk
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("wordnet")

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

verb_codes = {"VB","VBN","VBG","VBD","VBP","VBZ"}

def preprocessed_sentence(text):
    processed_text=[]
    text=text.lower()
    words=nltk.word_tokenize(text)
    tags = nltk.pos_tag(words)

    for i,word in enumerate(words):
        if tags[i][1] in verb_codes:
            lemmatized = lemmatizer.lemmatize(word,'v')
        else:
            lemmatized = lemmatizer.lemmatize(word)

        if lemmatized not in stop_words and lemmatized.isalpha():
            processed_text.append(lemmatized)

    final_sentence = "".join(processed_text)
    return final_sentence

final_data['processed description']=final_data['description'].apply(preprocessed_sentence)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidfvector = TfidfVectorizer()
tfidf_movieDes = tfidfvector.fit_transform(final_data["processed description"])

from sklearn.metrics.pairwise import cosine_similarity
cos_sim = cosine_similarity(tfidf_movieDes,tfidf_movieDes)

indices = pd.Series(final_data.index,index=final_data['title'])

def movie_recommendation(title,cosine_sim=cos_sim):
    title = title.strip().lower()
    cleaned_titles = indices.index.str.strip().str.lower()
    recommended_movie = []

    if title not in cleaned_titles.values:
        return []

    index = indices[title== cleaned_titles].iloc[0]
    similarit_score = pd.Series(cosine_sim[index]).sort_values(ascending=False)
    top_5_movies = list(similarit_score.iloc[1:6].index)

    for i in top_5_movies:
        recommended_movie.append(final_data['title'].iloc[i])

    return recommended_movie
