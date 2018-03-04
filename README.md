# Where is the answer? (Cevap Nerede ?)

This project is my junior project at Yildiz Technical University Computer Engineering Department and its advised by Asst.Prof. M. Fatih Amasyalı.
Basically this code compare the performances of some basic NLP methods on finding place of the answer. 
According to results we discuss the performance of various methods. Which one is the most effective to find where is the answer on a text.

We used Turkish Child Stories as test set. This set contains 500 questions and 71 stories in different size and difficulties.
According to this sets we implement very basic algorithms listed above.

### Method 0: Select Randomly
This is provement thesis for our hypothesis. At this method we select random sentences into text and returns as answer.
This might be our base-line and we tried to improve within next methods.

### Method 1: Basic Word Sameness
Counts same words in each sentences of text. The idea behind this method is "If a sentence contains same words with question it might be real answer."

### Method 2: First Six Characters Similarity
Turkish is suffix based language most root words are contains 6 letter. Therefore we compare words within six letters.
And the performance is getting more.

### Method 3: Constructing sentence vectors with FastText
We decided to use fasttext to get word embeddings. We used wiki.tr (compiled by FastText team from Turkish Wikipedia) file as train set.
When we got word embeddings,we constructed sentences as arithmetical average of words. First we created word vectors and then we sum all the words.
Finally we calculated the arithmetic average to get average vector and this vector represents the whole sentence.

To find similarity between sentences and question we used cosine similarity. This method approaches sentences as atomic units.  

### Method 4: Jaccard Similarity
We implemented jaccard similarity into words to find where is the answer.

### Method 5: Constructing word vectors with FastText (cosine similarity)
To increase performance we tried new method. In this method we approach words as atomic unis of a text. We calculate similarity of question and sentence texts using cosine similarity.

### Method 6: Constructing word vectors with FastText (euclidean similarity)
Uses similar with method5 algorithm to find word embeddings but this method use euclidean similarity to compare sentences. 
