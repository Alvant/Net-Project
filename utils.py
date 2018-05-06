import os
import pickle
import re
import numpy as np
import gensim
from gensim.models import KeyedVectors

RESOURCE_PATH = {
    'GOOGLE_EMBEDDINGS_PATH': os.path.join('data', 'GoogleNews-vectors-negative300.bin'),
    'STARSPACE_EMBEDDINGS_PATH': os.path.join('data', 'StarSpaceModelCornell.tsv'),
    'QA_FILE_TXT_PATH': os.path.join('data', 'data_prepared_cornell.txt')
}


def text_prepare(text):
    """Performs tokenization and simple preprocessing."""
    
    replace_by_space_re = re.compile('[/(){}\[\]\|@,;]')
    bad_symbols_re = re.compile('[^0-9a-z #+_]')

    text = text.lower()
    text = replace_by_space_re.sub(' ', text)
    text = bad_symbols_re.sub('', text)
    text = ' '.join([x for x in text.split() if x])

    return text.strip()


def load_embeddings(embeddings_path):
    if embeddings_path == RESOURCE_PATH['GOOGLE_EMBEDDINGS_PATH']:
        return load_google_embeddings(embeddings_path)
    elif embeddings_path == RESOURCE_PATH['STARSPACE_EMBEDDINGS_PATH']:
        return load_starspace_embeddings(embeddings_path)
    else:
        return None


def load_google_embeddings(embeddings_path):
    """Loads pre-trained word embeddings from tsv file.

    Args:
      embeddings_path - path to the embeddings file.

    Returns:
      embeddings - dict mapping words to vectors;
      embeddings_dim - dimension of the vectors.
    """

    embeddings = KeyedVectors.load_word2vec_format(
        embeddings_path,
        binary=True
    )

    dim = embeddings['dog'].size

    return embeddings


def load_starspace_embeddings(embeddings_path):
    embeddings = {}

    with open(embeddings_path, 'r') as f:
        lines = f.readlines()
    for l in lines:
        l = l.strip().split()
        if len(l) <= 1:
            continue
        embeddings[l[0]] = np.array([float(el) for el in l[1:]])

    dim = 0
    if embeddings:
        dim = len( embeddings[list(embeddings.keys())[0]] )

    return embeddings


def question_to_vec(question, embeddings):
    """Transforms a string to an embedding by averaging word embeddings."""

    dim = embeddings['dog'].size
    result = np.zeros((dim,))

    words = question.split(' ')

    count = 0
    for word in words:
        if word not in embeddings or not len(embeddings[word]):
            continue
        result += embeddings[word][:dim]
        count += 1

    return result / max(count, 1)


def unpickle_file(filename):
    """Returns the result of unpickling the file content."""

    with open(filename, 'rb') as f:
        return pickle.load(f)
