from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    documents = dict()
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename)) as f:
                documents[filename] = f.read()
        else:
            raise ValueError('Only txt files allowed!')
    return documents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    stop_puncuation = []
    for mark in list(string.punctuation):
        stop_puncuation.append(mark)
        stop_puncuation.append(mark + mark)
    stops = stopwords.words('english')
    stops.extend(stop_puncuation)
    words = [word.lower() for word in word_tokenize(document) if word not in stops]
    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    num_documents = len(list(documents.keys()))
    for name, text in documents.items():
        for word in text:
            num_documents_word_appears_in = count_word_in_documents(documents, word)
            idf = math.log(num_documents / num_documents_word_appears_in)
            idfs[word] = idf
    return idfs

def count_word_in_documents(documents, word):
    count = 0
    for text in documents.values():
        if word in text:
            count += 1
    return count


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    cum_tf_idf = dict()
    for filename, text in files.items():
        if filename not in list(cum_tf_idf.keys()):
            cum_tf_idf[filename] = 0
        for word in query:
            if word in text:
                num_times_in_text = text.count(word)
                # num_words_in_text = len(list(set(text)))
                # tf = num_times_in_text / num_words_in_text
                # idf = idfs[word]
                tf_idf = num_times_in_text * idfs[word]
                cum_tf_idf[filename] += tf_idf

    # sorted_cum_tf_idf = [key for key,value in sorted(cum_tf_idf.items(), key=lambda item : item[1])]
    # reversed_cum_tf_idf = sorted_cum_tf_idf[::-1]
    return sorted(cum_tf_idf, key=cum_tf_idf.get)[::-1][:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    cum_sentence_values = dict()
    for word in query:
        for s_key, sentence in sentences.items():
            if s_key not in cum_sentence_values.keys():
                cum_sentence_values[s_key] = 0
            if word in sentence:
                cum_sentence_values[s_key] += idfs[word]
    return sorted(cum_sentence_values, key=cum_sentence_values.get)[::-1][:n]

if __name__ == "__main__":
    main()
