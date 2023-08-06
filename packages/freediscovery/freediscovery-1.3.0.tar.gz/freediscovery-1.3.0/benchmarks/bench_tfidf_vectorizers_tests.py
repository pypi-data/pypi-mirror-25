"""

To run this benchmark, you will need,

 * scikit-learn
 * pandas
 * memory_profiler
 * psutil (optional, but recommended)

"""

from __future__ import print_function

import numbers
import timeit
import itertools
import sys

from tqdm import tqdm
import numpy as np
import pandas as pd
from memory_profiler import memory_usage
import scipy.sparse as sp

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import (CountVectorizer, TfidfVectorizer,
                                             HashingVectorizer, strip_accents_ascii,
                                             strip_accents_unicode, defaultdict,
                                             _make_int_array)
from cytoolz import identity, compose, juxt, concat, frequencies, unique, count, merge
from cytoolz.curried import curry, sliding_window, map as cmap, remove, get_in
import toolz
from toolz.sandbox.core import unzip
from cytoolz.curried import keymap

n_repeat = 3


class FastCountVectorizer(CountVectorizer):
    """Convert a collection of text documents to a matrix of token counts
    This implementation produces a sparse representation of the counts using
    scipy.sparse.csr_matrix.
    If you do not provide an a-priori dictionary and you do not use an analyzer
    that does some kind of feature selection then the number of features will
    be equal to the vocabulary size found by analyzing the data.
    Read more in the :ref:`User Guide <text_feature_extraction>`.
    Parameters
    ----------
    input : string {'filename', 'file', 'content'}
        If 'filename', the sequence passed as an argument to fit is
        expected to be a list of filenames that need reading to fetch
        the raw content to analyze.
        If 'file', the sequence items must have a 'read' method (file-like
        object) that is called to fetch the bytes in memory.
        Otherwise the input is expected to be the sequence strings or
        bytes items are expected to be analyzed directly.
    encoding : string, 'utf-8' by default.
        If bytes or files are given to analyze, this encoding is used to
        decode.
    decode_error : {'strict', 'ignore', 'replace'}
        Instruction on what to do if a byte sequence is given to analyze that
        contains characters not of the given `encoding`. By default, it is
        'strict', meaning that a UnicodeDecodeError will be raised. Other
        values are 'ignore' and 'replace'.
    strip_accents : {'ascii', 'unicode', None}
        Remove accents during the preprocessing step.
        'ascii' is a fast method that only works on characters that have
        an direct ASCII mapping.
        'unicode' is a slightly slower method that works on any characters.
        None (default) does nothing.
    analyzer : string, {'word', 'char', 'char_wb'} or callable
        Whether the feature should be made of word or character n-grams.
        Option 'char_wb' creates character n-grams only from text inside
        word boundaries; n-grams at the edges of words are padded with space.
        If a callable is passed it is used to extract the sequence of features
        out of the raw, unprocessed input.
    preprocessor : callable or None (default)
        Override the preprocessing (string transformation) stage while
        preserving the tokenizing and n-grams generation steps.
    tokenizer : callable or None (default)
        Override the string tokenization step while preserving the
        preprocessing and n-grams generation steps.
        Only applies if ``analyzer == 'word'``.
    ngram_range : tuple (min_n, max_n)
        The lower and upper boundary of the range of n-values for different
        n-grams to be extracted. All values of n such that min_n <= n <= max_n
        will be used.
    stop_words : string {'english'}, list, or None (default)
        If 'english', a built-in stop word list for English is used.
        If a list, that list is assumed to contain stop words, all of which
        will be removed from the resulting tokens.
        Only applies if ``analyzer == 'word'``.
        If None, no stop words will be used. max_df can be set to a value
        in the range [0.7, 1.0) to automatically detect and filter stop
        words based on intra corpus document frequency of terms.
    lowercase : boolean, True by default
        Convert all characters to lowercase before tokenizing.
    token_pattern : string
        Regular expression denoting what constitutes a "token", only used
        if ``analyzer == 'word'``. The default regexp select tokens of 2
        or more alphanumeric characters (punctuation is completely ignored
        and always treated as a token separator).
    max_df : float in range [0.0, 1.0] or int, default=1.0
        When building the vocabulary ignore terms that have a document
        frequency strictly higher than the given threshold (corpus-specific
        stop words).
        If float, the parameter represents a proportion of documents, integer
        absolute counts.
        This parameter is ignored if vocabulary is not None.
    min_df : float in range [0.0, 1.0] or int, default=1
        When building the vocabulary ignore terms that have a document
        frequency strictly lower than the given threshold. This value is also
        called cut-off in the literature.
        If float, the parameter represents a proportion of documents, integer
        absolute counts.
        This parameter is ignored if vocabulary is not None.
    max_features : int or None, default=None
        If not None, build a vocabulary that only consider the top
        max_features ordered by term frequency across the corpus.
        This parameter is ignored if vocabulary is not None.
    vocabulary : Mapping or iterable, optional
        Either a Mapping (e.g., a dict) where keys are terms and values are
        indices in the feature matrix, or an iterable over terms. If not
        given, a vocabulary is determined from the input documents. Indices
        in the mapping should not be repeated and should not have any gap
        between 0 and the largest index.
    parallel : {bool, str}, default=False
        use parallel dask computations when needed
    binary : boolean, default=False
        If True, all non zero counts are set to 1. This is useful for discrete
        probabilistic models that model binary events rather than integer
        counts.
    dtype : type, optional
        Type of the matrix returned by fit_transform() or transform().
    Attributes
    ----------
    vocabulary_ : dict
        A mapping of terms to feature indices.
    stop_words_ : set
        Terms that were ignored because they either:
          - occurred in too many documents (`max_df`)
          - occurred in too few documents (`min_df`)
          - were cut off by feature selection (`max_features`).
        This is only available if no vocabulary was given.
    See also
    --------
    HashingVectorizer, TfidfVectorizer
    Notes
    -----
    The ``stop_words_`` attribute can get large and increase the model size
    when pickling. This attribute is provided only for introspection and can
    be safely removed using delattr or set to None before pickling.
    """

    def __init__(self, input='content', encoding='utf-8',
                 decode_error='strict', strip_accents=None,
                 lowercase=True, preprocessor=None, tokenizer=None,
                 stop_words=None, token_pattern=r"(?u)\b\w\w+\b",
                 ngram_range=(1, 1), analyzer='word',
                 max_df=1.0, min_df=1, max_features=None,
                 vocabulary=None, binary=False, dtype=np.int64,
                 parallel=True):
        self.input = input
        self.encoding = encoding
        self.decode_error = decode_error
        self.strip_accents = strip_accents
        self.preprocessor = preprocessor
        self.tokenizer = tokenizer
        self.analyzer = analyzer
        self.lowercase = lowercase
        self.token_pattern = token_pattern
        self.stop_words = stop_words
        self.max_df = max_df
        self.min_df = min_df
        if max_df < 0 or min_df < 0:
            raise ValueError("negative value for max_df or min_df")
        self.max_features = max_features
        if max_features is not None:
            if (not isinstance(max_features, numbers.Integral) or
                    max_features <= 0):
                raise ValueError(
                    "max_features=%r, neither a positive integer nor None"
                    % max_features)
        self.ngram_range = ngram_range
        self.vocabulary = vocabulary
        self.binary = binary
        self.dtype = dtype
        self.parallel = parallel

    def build_preprocessor(self):
        """Return a function to preprocess the text before tokenization"""
        if self.preprocessor is not None:
            return self.preprocessor

        # unfortunately python functools package does not have an efficient
        # `compose` function that would have allowed us to chain a dynamic
        # number of functions. However the cost of a lambda call is a few
        # hundreds of nanoseconds which is negligible when compared to the
        # cost of tokenizing a string of 1000 chars for instance.

        # accent stripping
        if not self.strip_accents:
            strip_accents = identity
        elif callable(self.strip_accents):
            strip_accents = self.strip_accents
        elif self.strip_accents == 'ascii':
            strip_accents = strip_accents_ascii
        elif self.strip_accents == 'unicode':
            strip_accents = strip_accents_unicode
        else:
            raise ValueError('Invalid value for "strip_accents": %s' %
                             self.strip_accents)

        if self.lowercase:
            return compose(strip_accents, str.lower)
        else:
            return strip_accents

    def build_analyzer(self):
        """Return a callable that handles preprocessing and tokenization"""
        if callable(self.analyzer):
            return self.analyzer

        preprocess = self.build_preprocessor()

        if self.analyzer == 'char':
            return compose(self._char_ngrams, preprocess, self.decode)

        elif self.analyzer == 'char_wb':
            return compose(self._char_wb_ngrams, preprocess, self.decode)

        elif self.analyzer == 'word':
            stop_words = self.get_stop_words()
            tokenize = self.build_tokenizer()
            ngram_builder = self._word_ngrams(stop_words=stop_words)

            return compose(ngram_builder, tokenize, preprocess, self.decode)

        else:
            raise ValueError('%s is not a valid tokenization scheme/analyzer' %
                             self.analyzer)

    def _word_ngrams(self, stop_words=None):
        """Turn tokens into a sequence of n-grams after stop words filtering"""
        # handle stop words
        if stop_words is not None:
            stop_words_filter = remove(lambda x: x in stop_words)
        else:
            stop_words_filter = identity

        # handle token n-grams
        min_n, max_n = self.ngram_range
        if min_n == max_n == 1:
            return stop_words_filter
        else:
            return compose(concat,
                           juxt([compose(cmap(' '.join), sliding_window(ngram))
                                 for ngram in range(min_n, max_n+1)]),
                           stop_words_filter)

    def fit(self, raw_documents, y=None):
        """Learn a vocabulary dictionary of all tokens in the raw documents.
        Parameters
        ----------
        raw_documents : iterable
            An iterable which yields either str, unicode or file objects.
        Returns
        -------
        self
        """
        analyze = self.build_analyzer()
        if not self.parallel:
            res = list(compose(unique, concat, cmap(compose(unique, analyze)))(raw_documents))
        else:
            import dask.bag as db
            # version 2 => 2.38, 5.78
            seq = db.from_sequence(raw_documents, npartitions=5).map(analyze)
            def reduce_partitions(vectors):
                return set(el for row in vectors for el in row)
            res = seq.map_partitions(reduce_partitions).distinct().compute()

            # version 3 => 2.59, 26.64
            #seq = db.from_sequence(raw_documents, npartitions=5).map(compose(set, analyze))
            #res = sorted(list(seq.fold(set.union).compute()))

            #print(res)

        return self

    def _count_vocab(self, raw_documents, fixed_vocab):
        """Create sparse feature matrix, and vocabulary where fixed_vocab=False
        """
        vocabulary = {'test': 0, 'this': 1, 'etc': 2}
        #if fixed_vocab:
        #    vocabulary = self.vocabulary_
        #else:
        #    # Add a new value when a new vocabulary item is seen
        #    vocabulary = defaultdict()
        #    vocabulary.default_factory = vocabulary.__len__

        #analyze = self.build_analyzer()
        #j_indices = []
        #indptr = _make_int_array()
        #values = _make_int_array()
        #indptr.append(0)
        #for doc in raw_documents:
        #    feature_counter = {}
        #    for feature in analyze(doc):
        #        try:
        #            feature_idx = vocabulary[feature]
        #            if feature_idx not in feature_counter:
        #                feature_counter[feature_idx] = 1
        #            else:
        #                feature_counter[feature_idx] += 1
        #        except KeyError:
        #            # Ignore out-of-vocabulary items for fixed_vocab=True
        #            continue

        #    j_indices.extend(feature_counter.keys())
        #    values.extend(feature_counter.values())
        #    indptr.append(len(j_indices))

        #if not fixed_vocab:
        #    # disable defaultdict behaviour
        #    vocabulary = dict(vocabulary)
        #    if not vocabulary:
        #        raise ValueError("empty vocabulary; perhaps the documents only"
        #                         " contain stop words")

        #j_indices = np.asarray(j_indices, dtype=np.intc)
        #indptr = np.frombuffer(indptr, dtype=np.intc)
        #values = np.frombuffer(values, dtype=np.intc)

        #X = sp.csr_matrix((values, j_indices, indptr),
        #                  shape=(len(indptr) - 1, len(vocabulary)),
        #                  dtype=self.dtype)
        #X.sort_indices()

        analyze = self.build_analyzer()
        res = list(map(compose(frequencies, analyze), raw_documents))
        vocab = {key: idx for idx, key in enumerate(sorted(unique(concat(el.keys() for el in res))))}
        def token2id(token):
            return vocab[token]
        res2 = map(keymap(token2id), res)
        res3 = unzip((el.keys(), el.values()) for el in res2)
        
        indices = np.asarray(list(concat(res3[0])))
        data = np.asarray(list(concat(res3[1])))
        #print(indices)
        #print(vocab)
        X = sp.csr_matrix(np.ones((1, 3)))
        return vocabulary, X


vect = FastCountVectorizer(ngram_range=(1, 2))

analyzer = vect.build_analyzer()

#print(analyzer('This document thing'))

#sys.exit()


def run_vectorizer(Vectorizer, X, **params):
    def f():
        vect = Vectorizer(**params)
        vect.fit(X)
    return f


text = fetch_20newsgroups(subset='train').data#[:2000]

print("="*80 + '\n#' + "    Text vectorizers benchmark" + '\n' + '='*80 + '\n')
print("Using a subset of the 20 newsrgoups dataset ({} documents)."
      .format(len(text)))
print("This benchmarks runs in ~20 min ...")

res = []

for Vectorizer, (analyzer, ngram_range) in tqdm(itertools.product(
            [FastCountVectorizer, CountVectorizer],
            [('word', (1, 1)),
             #('word', (1, 2)),
             #('word', (1, 4)),
             #('char', (4, 4)),
             #('char_wb', (4, 4))
             ])):

    bench = {'vectorizer': Vectorizer.__name__}
    params = {'analyzer': analyzer, 'ngram_range': ngram_range}
    bench.update(params)
    dt = timeit.repeat(run_vectorizer(Vectorizer, text, **params),
                       number=1,
                       repeat=n_repeat)
    bench['time'] = "{:.2f} (+-{:.2f})".format(np.mean(dt), np.std(dt))

    mem_usage = memory_usage(run_vectorizer(Vectorizer, text, **params))

    bench['memory'] = "{:.1f}".format(np.max(mem_usage))

    res.append(bench)


df = pd.DataFrame(res).set_index(['analyzer', 'ngram_range', 'vectorizer'])

print('\n========== Run time performance (sec) ===========\n')
print('Computing the mean and the standard deviation '
      'of the run time over {} runs...\n'.format(n_repeat))
print(df['time'].unstack(level=-1))

print('\n=============== Memory usage (MB) ===============\n')
print(df['memory'].unstack(level=-1))
