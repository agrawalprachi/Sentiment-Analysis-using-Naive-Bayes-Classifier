# Sentiment-Analysis-using-Naive-Bayes-Classifier
 A naive Bayes classifier to identify hotel reviews as either true or fake, and either positive or negative. Word tokens are used as features for classification.

# Data
A set of training and development data is given.

File train-labeled.txt contains labeled training data with a single training instance (hotel review) per line (total 960 lines). The first 3 tokens in each line are:
a unique 7-character alphanumeric identifier
a label True or Fake
a label Pos or Neg
These are followed by the text of the review.
File dev-text.txt contains unlabeled development data, containing just the unique identifier followed by the text of the review (total 320 lines).
File dev-key.txt contains the corresponding labels for the development data, to serve as an answer key.

# Programs

nblearn.py will learn a naive Bayes model from the training data, and nbclassify.py will use the model to classify new data.

The program will learn a naive Bayes model, and write the model parameters to a file called nbmodel.txt.
The program nbclassify.py will read the parameters of a naive Bayes model from the file nbmodel.txt, classify each entry in the test data, and write the results to a text file called nboutput.txt in the same format as the answer key.
