import pandas as pd
from transformers import pipeline
import spacy
from itertools import islice

# ------------------------------ sentiment analyzer functions

def analyzer(text, sentiment_pipeline):
    result = sentiment_pipeline(text)[0]
    return result['label'], result['score']

def store_analysis(label, score):
    global positive, neutral, negative
    if label == 'LABEL_0':
        negative['counter'] += 1
        negative['sum_score'] += score
    elif label == 'LABEL_1':
        neutral['counter'] += 1
        neutral['sum_score'] += score
    elif label == 'LABEL_2':
        positive['counter'] += 1
        positive['sum_score'] += score

# ------------------------------ counter words and adjectives

def counter_words(text,nlp):
    global intCWords
    doc = nlp(text)
    for token in doc: 
        if token.text.isalpha():
            intCWords += 1
            word = token.text.lower()
            if word in countWords:
                increment_counter(word, token, 'exist')
            else:
                increment_counter(word, token, 'add')
            
def increment_counter(w, t, mode):
    global intCAdjs
    if mode=='exist':
        countWords[w] += 1
        if t.pos_ == "ADJ":
            intCAdjs += 1
            if w in countAdjs:
                countAdjs[w] += 1
            else:
                countAdjs[w] = 1

    elif mode=='add':
        countWords[w] = 1
        if t.pos_ == "ADJ":
            intCAdjs += 1
            if w in countAdjs:
                countAdjs[w] += 1
            else:
                countAdjs[w] = 1

# ------------------------------ statistics

def stats_generation():
    global countWords, countAdjs, intCWords, intCAdjs, positive, neutral, negative

    positive_counter = positive['counter']
    neutral_counter = neutral['counter']
    negative_counter = negative['counter']
    total_counter = positive_counter + neutral_counter + negative_counter

    positive_score = positive['sum_score']
    neutral_score = neutral['sum_score']
    negative_score = negative['sum_score']
    total_score = positive_score + neutral_score + negative_score

    positive_percentage = positive_counter/total_counter
    neutral_percentage = neutral_counter/total_counter
    negative_percentage = negative_counter/total_counter

    positive_avg_score = positive_score/positive_counter
    neutral_avg_score = neutral_score/neutral_counter
    negative_avg_score = negative_score/negative_counter

    positive_distribution = positive_score/total_score
    neutral_distribution = neutral_score/total_score
    negative_distribution = negative_score/total_score

    positive_output =  {'percentage': round(positive_percentage*100,2),
                        'counter': positive_counter,
                        'average_score': round(positive_avg_score,2),
                        'distribution': round(positive_distribution*100,2)}

    neutral_output =  {'percentage': round(neutral_percentage*100,2),
                        'counter': neutral_counter,
                        'average_score': round(neutral_avg_score,2),
                        'distribution': round(neutral_distribution*100,2)}

    negative_output =  {'percentage': round(negative_percentage*100,2),
                        'counter': negative_counter,
                        'average_score': round(negative_avg_score,2),
                        'distribution': round(negative_distribution*100,2)}

    return positive_output, neutral_output, negative_output

# ------------------------------ from dataframe to percentages and quantity

def data_processing(df, column_name, pipeline):
    global countWords, countAdjs, intCWords, intCAdjs, positive, neutral, negative
    countWords = {}
    countAdjs = {}
    intCWords = 0
    intCAdjs = 0
    positive = {'counter':0, 'sum_score':0}
    neutral = {'counter':0, 'sum_score':0}
    negative = {'counter':0, 'sum_score':0}

    nlp = spacy.load("en_core_web_sm")

    for row_index, row in df.iterrows():
        text = row[column_name]
        label, score = analyzer(text, pipeline)
        print(row_index)
        store_analysis(label, score)
        counter_words(text, nlp)

    positive_out, neutral_out, negative_out = stats_generation()
    most_repeated_adjs = dict(
                            islice(
                                sorted(
                                    countAdjs.items(), key=lambda x: x[1], reverse=True
                                )
                                ,5
                            )
                        )
    text_stats = [row_index, intCWords, intCAdjs, intCWords//row_index]

    return positive_out, neutral_out, negative_out, most_repeated_adjs, text_stats

# ------------------------------ main

if __name__ == '__main__':
    print("Analizando textos")
