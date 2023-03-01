import itertools
import random
import string

import pandas as pd


def randomlyChangeNNum(word, value):
    length = len(word)
    word = list(word)
    k = random.sample(range(0, length), value)
    for index in k:
        word[index] = random.choice(string.digits)
    return "".join(word)


def randomlyAddNNum(word, value):
    length = len(word)
    word = list(word)
    k = random.sample(range(0, length), value)
    for index in k:
        word.insert(index, random.choice(string.digits))
    return "".join(word)


def randomlyRemoveNNum(word, value):
    length = len(word)
    word = list(word)
    k = random.sample(range(0, length), value)
    k.sort(reverse=True)
    for index in k:
        word.pop(index)
    return "".join(word)


def randomPerurbationNNum(word, value):
    list1 = [1, 2, 3]
    index = random.choice(list1)
    if index == 1:
        return randomlyChangeNNum(word, value)
    if index == 2:
        return randomlyAddNNum(word, value)
    if index == 3:
        return randomlyRemoveNNum(word, value)


def randomlyChangeNChar(word, value):
    length = len(word)
    word = list(word)
    k = random.sample(range(0, length), value)
    for index in k:
        word[index] = random.choice(string.ascii_lowercase)
    return "".join(word)


def randomlyAddNChar(word, value):
    length = len(word)
    word = list(word)
    k = random.sample(range(0, length), value)
    for index in k:
        word.insert(index, random.choice(string.ascii_lowercase))
    return "".join(word)


def randomlyRemoveNChar(word, value):
    length = len(word)
    word = list(word)
    k = random.sample(range(0, length), value)
    k.sort(reverse=True)
    for index in k:
        word.pop(index)
    return "".join(word)


def randomPerurbationNChar(word, value):
    list1 = [1, 2, 3]
    index = random.choice(list1)
    if index == 1:
        return randomlyChangeNChar(word, value)
    if index == 2:
        return randomlyAddNChar(word, value)
    if index == 3:
        return randomlyRemoveNChar(word, value)


df = pd.read_csv("compas-scores-raw_.csv").head(1000)
col1 = ['left_' + col for col in df.columns]
col2 = ['right_' + col for col in df.columns]
col = col1 + col2
col.append('match')

li = []
for i in range(len(df.index)):
    for j in range(i, len(df.index)):
        item = [df.iloc[i].values.flatten().tolist(), df.iloc[j].values.flatten().tolist()]

        item[1][5] = randomPerurbationNChar(item[1][5], 1)
        item[1][6] = randomPerurbationNChar(item[1][6], 1)
        item[1][10] = randomPerurbationNNum(item[1][10], 1)

        if df.iloc[i]['Person_ID'] == df.iloc[j]['Person_ID']:
            item.append([1])
        else:
            item.append([0])
        li.append(list(itertools.chain(*item)))

df2 = pd.DataFrame(data=li, columns=col)
df2 = df2.drop(
    ['left_Person_ID', 'left_AssessmentID', 'left_Case_ID', 'right_Person_ID', 'right_AssessmentID', 'right_Case_ID'],
    axis=1)

df2.to_csv('compas_for_em.csv', index=False)
