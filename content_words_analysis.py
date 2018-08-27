# -*- coding: utf-8 -*-
from scasim import scasim

import pandas as pd
import math
import nltk


df = pd.read_excel('/Users/jenni/PycharmProjects/Scasim/venv/fixations_shared_sample_edited.xlsx')

people = tuple(df['RECORDING_SESSION_LABEL'].tolist())
sentences = tuple(df['CURRENT_FIX_INDEX'].tolist())
IA_left = tuple(df['IA_LEFT'].tolist())
IA_right = tuple(df['IA_RIGHT'].tolist())
word = tuple(df['CURRENT_FIX_INTEREST_AREA_INDEX'].tolist())
words_of_sentence = tuple(df['CURRENT_FIX_INTEREST_AREA_LABEL'].tolist())
actual_sentences = tuple(df['sentence'].tolist())


#Create the list of tuples.

import csv
with open('/Users/jenni/PycharmProjects/Scasim/venv/fixations_shared_sample_edited.csv') as f:

    data1 = [list(line) for line in csv.reader(f)]
    data_tuples = []
    for linelist in data1:
        linelist = tuple(map(float, linelist))
        data_tuples.append(linelist)
    #print(data_tuples)
    
#Create list of sentence boundaries, and separate data_tuples by sentence boundaries. Also compile a list of the actual sentences.
sentence_boundaries = [0]
actual_sentences_list = [actual_sentences[0]]

for i in range(len(sentences)-1):
    if sentences[i+1] != sentences[i] and sentences[i+1] == 1:
        sentence_boundaries.append(i+1)
        actual_sentences_list.append(actual_sentences[i+1])
        if isinstance(actual_sentences[i+1], float):
            if math.isnan(actual_sentences[i+1]):
                actual_sentences_list.pop()
                actual_sentences_list.append(actual_sentences[i+2])

# 78 is used since it's the number of sentences in the file.

actual_sentences_list = actual_sentences_list[:78]


        
sentence_boundaries.append(None)
        
sentence_tuples = []

for i in range(len(sentence_boundaries)-1):
    
        sentence = data_tuples[sentence_boundaries[i]:sentence_boundaries[i+1]]
        sentence_tuples.append(sentence)

#Create list of reader boundaries relative to sentence boundaries. Then create list structure like [[st, st],[st, st, st]]—a list of
#lists of sentence_tuples elements, separated by reader.

people_boundaries = [0]

for i in range(len(sentence_boundaries)-2):
    if people[sentence_boundaries[i+1]] != people[sentence_boundaries[i]]:
        people_boundaries.append(i+1)
people_boundaries.append(None)


reader_sentence_tuples = []

for i in range(len(people_boundaries)-1):
    
        person = sentence_tuples[people_boundaries[i]:people_boundaries[i+1]]
        reader_sentence_tuples.append(person)
        


def remove_dup(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list
 
sentences_with_words = []



for i in range(78):
    sentence_words = list(words_of_sentence[sentence_boundaries[i]:sentence_boundaries[i+1]])
    length = len(sentence_words)
    for j in range(length):
        if sentence_words[length-1-j] == '.':
            del sentence_words[length-1-j]
    sentence_words = remove_dup(sentence_words)
    sentence_words[len(sentence_words)-1] = sentence_words[len(sentence_words)-1][:-1]
    sentences_with_words.append(sentence_words)


actual_sentences_list_pos = []
for i in actual_sentences_list:
    postag = nltk.pos_tag(nltk.word_tokenize(i))
    actual_sentences_list_pos.append(postag)

print((actual_sentences_list[57]))
tokens = nltk.word_tokenize((actual_sentences_list[57]))
print(tokens)
print(actual_sentences_list_pos[57])
x = actual_sentences_list_pos[57]
number = 0

actual_sentences_list_content = []
for i in actual_sentences_list_pos:
    content = 0
    for i in x:
        if (i[0] == "am" or i[0] == "is" or i[0] == "are" or i[0] == "be" or i[0] == "was" or i[0] == "were") == False:
        
            if i[1] == "CD" or i[1] == "FW" or i[1] == "JJ" or i[1] == "JJR" or i[1] == "JJS" or i[1] == "LS" or i[1] == "NN" or i[1] == "NNS":
                content +=1
            elif i[1] == "NNP" or i[1] == "NNPS" or i[1] == "RB" or i[1] == "RBR" or i[1] == "RBS" or i[1] == "SYM" or i[1] == "VB" or i[1] == "VBD":
                content +=1
            elif i[1] == "VBG" or i[1] == "VBN" or i[1] == "VBP" or i[1] == "VBZ":
                content +=1
    actual_sentences_list_content.append(content)
print(actual_sentences_list_content[57])

df2 = pd.DataFrame(actual_sentences_list_content)
df2.to_excel('actual_sentences_list_content.xlsx', header=False, index=False)
