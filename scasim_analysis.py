# scanpath-analysis

# -*- coding: utf-8 -*-

# This code analyzes the scanpath similarities between ESL test subjects and native English speakers.
#In here I assume every test subject reads the same sentences.
# This uses the program https://github.com/tmalsburg/scanpath/blob/master/Resources/scasim.py.

from scasim import scasim
import pandas as pd
import math
from pandas import DataFrame
import scipy

# df is for file containing the numerical data; df2 is for a file containing data on native languages of test subjects.

df = pd.read_excel('/Users/jenni/PycharmProjects/Scasim/venv/new_fixations_modified.xlsx')
df2 = pd.read_excel('/Users/jenni/PycharmProjects/Scasim/venv/metadata-jennifer.xlsx')

people = tuple(df['RECORDING_SESSION_LABEL'].tolist())
sentences = tuple(df['CURRENT_FIX_INDEX'].tolist())
IA_left = tuple(df['IA_LEFT_MOD'].tolist())
IA_right = tuple(df['IA_RIGHT_MOD'].tolist())
word = tuple(df['CURRENT_FIX_INTEREST_AREA_INDEX'].tolist())
sentence_ID = tuple(df['sentenceid'].tolist())

ID_2 = tuple(df2['ID'].tolist())
nativelang = tuple(df2['L1'].tolist())
michigan = tuple(df2['Michigan'].tolist())

#The .csv file is for the purely numerical data portion, with one column = x, one column = y, one column = duration.
#Create list of tuples.
import csv
with open('/Users/jenni/PycharmProjects/Scasim/venv/new_fixations_modified_csv.csv') as f:

    data1 = [list(line) for line in csv.reader(f)]
    data_tuples = []
    for linelist in data1:
        linelist = tuple(map(float, linelist))
        data_tuples.append(linelist)
    #print(data_tuples)
    
#Create list of sentence boundaries, and separate data_tuples by sentence boundaries.
sentence_boundaries = [0]

for i in range(len(sentences)-1):
    if sentences[i+1] == 1:
        sentence_boundaries.append(i+1)
        
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
'''
print(len(sentence_boundaries))
print(people_boundaries)
print(sentences[sentence_boundaries[16]])
print(sentence_boundaries[16])
print(sentences[528])
'''

reader_sentence_tuples = []

for i in range(len(people_boundaries)-1):
    
        person = sentence_tuples[people_boundaries[i]:people_boundaries[i+1]]
        reader_sentence_tuples.append(person)

#Compute the length of sentences.

len_sentences = []

for i in range(len(reader_sentence_tuples[0])):
    sentence_words = list(word[sentence_boundaries[i]:sentence_boundaries[i+1]])
    length = len(sentence_words)
    for j in range(length):
        if ((isinstance(sentence_words[length-1-j], int) == False)
        or math.isnan(sentence_words[length-1-j])): 
            del sentence_words[length-1-j]
    len_sentences.append(max(sentence_words))


#Get lists of native English speakers and ESL people, with respect to df. Only doing 1st - 182nd entries in ID_2.
#native_IDs and ESL_IDs are the indices, in ID_1, of the native and ESL test subjects. 

ID_1 = []
native_IDs = []
ESL_IDs = []

for i in range(len(people)-1):
    if people[i+1] != people[i]:
        ID_1.append(people[i])
ID_1.append(people[len(people)-1])

for i in range(len(nativelang)):
    if nativelang[i] == "English":
        native_IDs.append(ID_1.index(ID_2[i]))
    else:
        ESL_IDs.append(ID_1.index(ID_2[i]))

# Write the IDs of the ESL test subjects in Excel, if desired.
ID_of_ESL_all = []

for i in ESL_IDs:
    ID_of_ESL_all.append(ID_1[i])
        
df3 = pd.DataFrame(ID_of_ESL_all)
df3.to_excel('ID_of_ESL_all.xlsx', header=False, index=False)

# Write Michigan scores in Excel, if desired.

michigan_real = []
for element in michigan:
    if not(math.isnan(element)):
        michigan_real.append(element)

df4 = pd.DataFrame(michigan_real)
df4.to_excel('output1.xlsx', header=False, index=False)


#Do scasim analysis. Compute the average scasim similarity, for each ESL person, across sentences and across native people.

number_fixations_number_words = []

# If number of fixations = number of words
for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:len_sentences[k]], reader_sentence_tuples[j][k][:len_sentences[k]], 512, 0.01, 1805, 1)
    number_fixations_number_words.append(sum/(78*37))

df5 = pd.DataFrame(number_fixations_number_words)
df5.to_excel('output_all_fixations_is_words.xlsx', header=False, index=False)



l1 = []
l2 = []
l3 = []
l4 = []
l5 = []
l6 = []
l7 = []
l8 = []
l9 = []

ESL_native_scasim_all = []

# In here I am computing scasims for taking the first 4, 6, 8, 10, 12, 14, 16, 18, and 20 fixations of each sentence.
# I am also doing scasims if all fixations are taken into consideration, if desired.

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:4], reader_sentence_tuples[j][k][:4], 512, 0.01, 1805, 1)
    l1.append(sum/(78*37))

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:6], reader_sentence_tuples[j][k][:6], 512, 0.01, 1805, 1)
    l2.append(sum/(78*37))

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:8], reader_sentence_tuples[j][k][:8], 512, 0.01, 1805, 1)
    l3.append(sum/(78*37))
    
for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:10], reader_sentence_tuples[j][k][:10], 512, 0.01, 1805, 1)
    l4.append(sum/(78*37))

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:12], reader_sentence_tuples[j][k][:12], 512, 0.01, 1805, 1)
    l5.append(sum/(78*37))

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:14], reader_sentence_tuples[j][k][:14], 512, 0.01, 1805, 1)
    l6.append(sum/(78*37))

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:16], reader_sentence_tuples[j][k][:16], 512, 0.01, 1805, 1)
    l7.append(sum/(78*37))

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:18], reader_sentence_tuples[j][k][:18], 512, 0.01, 1805, 1)
    l8.append(sum/(78*37))

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k][:20], reader_sentence_tuples[j][k][:20], 512, 0.01, 1805, 1)
    l9.append(sum/(78*37))

for i in ESL_IDs:
    sum = 0
    for j in native_IDs:
        for k in range(len(reader_sentence_tuples[0])):
            sum += scasim(reader_sentence_tuples[i][k], reader_sentence_tuples[j][k], 512, 0.01, 1805, 1)
    ESL_native_scasim_all.append(sum/(78*37))

df6 = pd.DataFrame(ESL_native_scasim_all)
df6.to_excel('output_all_all.xlsx', header=False, index=False)

df7 = DataFrame({'4': l1, '6': l2, '8': l3,'10': l4,'12': l5,'14': l6,'16': l7,'18': l8,'20': l9 })

df7.to_excel('scasim_all_plots.xlsx', sheet_name='sheet1', index=False)


# Language similarity matrix.

ch_IDs = []
po_IDs = []
sp_IDs = []
ja_IDs = []

for i in range(len(nativelang)):
    if nativelang[i] == "Chinese":
        ch_IDs.append(ID_1.index(ID_2[i]))
    if nativelang[i] == "Portuguese":
        po_IDs.append(ID_1.index(ID_2[i]))
    if nativelang[i] == "Spanish":
        sp_IDs.append(ID_1.index(ID_2[i]))
    if nativelang[i] == "Japanese":
        ja_IDs.append(ID_1.index(ID_2[i]))
        

        
ESL_IDs2 = [ch_IDs, po_IDs, sp_IDs, ja_IDs]

ESL_scasim_matrix = [[0 for x in range(4)] for y in range(4)]

for lang1 in ESL_IDs2:
    sum = 0
    for lang2 in ESL_IDs2:
        sum = 0
        for i in lang1:
            for j in lang2:
                for k in range(len(reader_sentence_tuples[0])):
                    sum += scasim(reader_sentence_tuples[i][k][:8], reader_sentence_tuples[j][k][:8], 512, 0.01, 1805, 1)
        ESL_scasim_matrix[ESL_IDs2.index(lang1)][ESL_IDs2.index(lang2)] = sum/(len(reader_sentence_tuples[0])*len(lang1)*len(lang2))
