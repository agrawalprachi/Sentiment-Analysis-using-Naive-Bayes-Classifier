import sys
import json
import re
import string
import math

infile = sys.argv[1]
data = json.load(open('nbmodel.txt'))
word_prob_dict = data["dictionary"]
prior_fake = data["prior_fake"]
prior_true = data["prior_true"]
prior_pos = data["prior_pos"]
prior_neg = data["prior_neg"]

ofile = open("nboutput.txt", "w")

tr = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

with open(infile) as f:
    for line in f:
        line = line.strip()
        line = line.translate(tr)
        #line = re.sub(r'[^\w\s]', '', line)
        words = line.split(" ")

        pos_prob = math.log(prior_pos)
        neg_prob = math.log(prior_neg)
        fake_prob = math.log(prior_fake)
        true_prob = math.log(prior_true)

        answer_sentence = words[0]
        for word in words[1:]:
            word = word.lower()
            if word in word_prob_dict:
                pos_prob = pos_prob + math.log(word_prob_dict[word][0][1])
                neg_prob = neg_prob + math.log(word_prob_dict[word][1][1])
                true_prob = true_prob + math.log(word_prob_dict[word][2][1])
                fake_prob = fake_prob + math.log(word_prob_dict[word][3][1])

        if true_prob > fake_prob:
                answer_sentence = answer_sentence + " True"
        else:
            answer_sentence = answer_sentence + " Fake"

        if pos_prob > neg_prob:
                answer_sentence = answer_sentence + " Pos"
        else:
            answer_sentence = answer_sentence + " Neg"

        answer_sentence = answer_sentence + "\n"
        ofile.write(answer_sentence)