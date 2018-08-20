import sys
import json
import string

infile = sys.argv[1]

fakeCount = 0
trueCount = 0
posCount = 0
negCount = 0
vocabulary = set()
positive = {}
negative = {}
fake = {}
true = {}
import re

# stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
#                 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
#                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#                 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
#                 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
#                 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
#                 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
#                 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
#                 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only'
#         , 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

stop_words=     ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                'until', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'only',
                 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
                 'us', 'much', 'would', 'either', 'indeed', 'seems']


tr = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

with open(infile) as f:
    for line in f:
        line  = line.strip()
        line = line.translate(tr)
        #line = re.sub(r'[^\w\s]', '', line)
        words = line.split(" ")

        if words[1].strip() == "Fake":
            fakeCount += 1
        if words[1].strip() == "True":
            trueCount += 1
        if words[2].strip() == "Pos":
            posCount += 1
        if words[2].strip() == "Neg":
            negCount += 1

        for word in words[3:]:
            word = word.lower()
            if words[1].strip() == "Fake" and word not in stop_words:
                if word not in fake:
                    fake[word] = 1
                else:
                    fake[word] += 1
                vocabulary.add(word);

            if words[1].strip() == "True" and word not in stop_words:
                if word not in true:
                    true[word] = 1
                else:
                    true[word] += 1
                vocabulary.add(word);

            if words[2].strip() == "Pos" and word not in stop_words:
                if word not in positive:
                    positive[word] = 1
                else:
                    positive[word] += 1
                vocabulary.add(word);

            if words[2].strip() == "Neg" and word not in stop_words:
                if word not in negative:
                    negative[word] = 1
                else:
                    negative[word] += 1
                vocabulary.add(word);


prior_fake = fakeCount/float(fakeCount+trueCount)
prior_true = trueCount/float(fakeCount+trueCount)
prior_pos = posCount/float(posCount+negCount)
prior_neg = negCount/float(posCount+negCount)

word_prob_dict = {}

for word in vocabulary:

    word_prob_dict[word] = []

    numerator = 1
    if word in positive:
        numerator += positive[word]
    word_prob_dict[word].append(('pos', numerator / float(len(vocabulary) + sum(positive.values()))))

    numerator = 1
    if word in negative:
        numerator += negative[word]
    word_prob_dict[word].append(('neg', numerator / float(len(vocabulary) + sum(negative.values()))))

    numerator = 1
    if word in true:
        numerator += true[word]
    word_prob_dict[word].append(('true', numerator / float(len(vocabulary) + sum(true.values()))))

    numerator = 1
    if word in fake:
        numerator += fake[word]
    word_prob_dict[word].append(('fake', numerator / float(len(vocabulary) + sum(fake.values()))))


data = {"dictionary" : word_prob_dict, "prior_fake": prior_fake,  "prior_true": prior_true, "prior_pos" : prior_pos, "prior_neg" : prior_neg}
json = json.dumps(data)
f = open("nbmodel.txt","w")
f.write(json)
f.close()