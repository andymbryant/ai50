from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
import sys
import os
import math
import operator

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
    # Loop through filenames in directory
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            # Read the contents of the file into the documents dict
            documents[filename] = f.read()
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
        # stop_puncuation.append(mark + mark)
        # stop_puncuation.append(mark + mark + mark + mark)
    stops = stopwords.words('english')
    # Add punctuation marks to the stop words list
    stops.extend(stop_puncuation)
    # Tokenize the words, remove those that are in the stops list, and make them lowercase
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
            # Get the number of times a word appears in all of the documents
            num_documents_word_appears_in = count_word_in_documents(documents, word)
            # Calculate idf and add it to the idfs dict
            idf = math.log(num_documents / num_documents_word_appears_in)
            idfs[word] = idf
    return idfs

def count_word_in_documents(documents, word):
    '''
    Helper function for counting the amount of times a word appears in the all of the documents.
    '''
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
        # Add filename to the cum_tf_idf if it does not exist to avoid key error
        if filename not in list(cum_tf_idf.keys()):
            cum_tf_idf[filename] = 0
        for word in query:
            # If the word in the query appears in the text, calculate tf_idf
            # NOTE: this formula for tf_idf is different than the one provided in the specifications
            if word in text:
                # Get tf
                num_times_in_text = text.count(word)
                num_words_in_text = len(list(set(text)))
                tf = num_times_in_text / num_words_in_text
                # Multiply tf by idf
                idf = idfs[word]
                tf_idf = tf * idf
                cum_tf_idf[filename] += tf_idf
    # Sort the files by their tf_idf
    sorted_files = sorted(cum_tf_idf, reverse=True, key=cum_tf_idf.get)
    top_files = sorted_files[:n]
    return top_files

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
        # Loop through the sentences, isolating the sentence as
        for s_key, s_values in sentences.items():
            # If sentence key not found, initialize with 0 values for idf and qtd
            if s_key not in cum_sentence_values.keys():
                cum_sentence_values[s_key] = {
                    'idf': 0,
                    'qtd': 0
                }
            if word in s_values:
                # Increment idf values
                cum_sentence_values[s_key]['idf'] += idfs[word]
                # Calculate qtd, which is the number of words in the sentence that are also in the query
                qtd = len([s_word for s_word in s_values if s_word in query]) / len(s_values)
                # Add qtd values
                cum_sentence_values[s_key]['qtd'] = qtd
    # Sort by idf and qtd
    sorted_sentences = sorted(cum_sentence_values.keys(), reverse=True, key=lambda x: (cum_sentence_values[x]['idf'], cum_sentence_values[x]['qtd']))
    top_sentences = sorted_sentences[:n]
    return top_sentences

if __name__ == "__main__":
    main()
