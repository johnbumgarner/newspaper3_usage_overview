#!/usr/bin/env python3

"""
This Python script is designed to perform various types of Natural Language
processing tasks.

Module used: NLTK
Module Reference: https://www.nltk.org

NLTK functions:
1. Part of Speech tagging
2. Frequency of words
3. Most common words
4. Tokenization
5. Adjectives
6. Pronouns
7. Adverbs
8. Verbs
9. Nouns
10. NGRAMS
"""
__author__ = 'John Bumgarner'
__status__ = 'Production'
__date__ = 'October 11, 2018'

##################################################################################
# Python imports required for basic operations
##################################################################################
import re as regex
from nltk import ngrams
from nltk import FreqDist
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

# this module is needed to remove punctuation characters
from string import punctuation

# ASCII characters which are considered punctuation characters.
# These characters will be removed from the text
exclude_punctuation = set(punctuation)

# NLTK has these stop words languages available
# 'arabic', 'azerbaijani', 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'greek', 
# 'hungarian', 'indonesian', 'italian', 'kazakh', 'nepali', 'norwegian', 'portuguese', 'romanian', 
# 'russian', 'slovene', 'spanish', 'swedish', 'tajik', 'turkish']
#
# English stop words to remove from text.
# A stop word is a commonly used word, such
# as “the”, “a”, “an”, “in”
stop_words = set(stopwords.words('english'))


class NLPCustomMethods:

    @classmethod
    def expunge_punctuations(cls, textual_data):
        """
        This function is used normalized text from the submitted textual information.
        This process will lowercase all the words in the provided text.
        All common punctuations will be removed from text.
        :param textual_data: Textual information
        :return: normalized text with punctuations removed
        """
        normalized = ''.join([i for i in textual_data.lower() if i not in exclude_punctuation])
        return normalized

    @classmethod
    def expunge_stopwords(cls, textual_data):
        """
        This function is used normalized text from the submitted textual information.
        This process will lowercase all the words in the provided text.
        All English stop words will be removed from text.
        :param textual_data: Textual information
        :return: normalized text with stopwords removed
        """
        normalized = ' '.join([i for i in regex.split('[\'| ]', ''.join(textual_data).lower()) if i not in stop_words])
        return normalized

    @classmethod
    def get_sentences(cls, textual_data):
        """
        This function is used to extract sentences from the submitted textual information.
        The sentences are split based on punctuation.
        :param textual_data: Textual information
        :return: extracted sentences
        :rtype: list
        """
        sentences = sent_tokenize(textual_data.lower())
        return sentences

    @classmethod
    def get_wordpunct(cls, textual_data):
        """
        This function is used to split sentences based on the punctuations and words in the submitted
        textual information. The splitting is based on a simple regexp tokenization process.
        :param textual_data: Textual information
        :return: split sentences based on punctuation
        :rtype: list
        """
        words = wordpunct_tokenize(textual_data.lower())
        return words

    @classmethod
    def get_ngrams(cls, textual_data, n):
        """
        This function is used to produce N-Grams from the submitted textual information.
        N-Grams are simply a sequence of words.
        For example:
            Batman - is 1-grams (aka unigrams)
            Gotham City - is 2-grams (aka bigrams)
            The Three Musketeers - is 3-grams (aka trigrams)
            Up up and away - is a 4-grams
        :param textual_data: Textual information
        :param n: The number of n-grams to produce from the input.
        :return: n-grams
        :rtype: list
        """
        n_grams = ngrams(word_tokenize(textual_data.lower()), n)
        return [' '.join(grams) for grams in n_grams]

    @classmethod
    def get_most_common_words(cls, textual_data, n):
        """
        This function is used to extract the most common words from the submitted textual information.
        :param textual_data: Textual information
        :param n: The number of words to extract from the input.
        :return: The most common words from the input.
        :rtype: list
        """
        words = word_tokenize(textual_data.lower())
        frequency_distribution = FreqDist(words)
        most_common = frequency_distribution.most_common(n)
        return most_common

    @classmethod
    def get_frequency_distribution(cls, textual_data, number_of_words_to_return):
        """
        This function is used to produce the frequency of words from the submitted textual information.
        :param textual_data: Textual information
        :param number_of_words_to_return: int value
        :return: the frequency of x number of words
        :rtype: list
        """
        tokens = word_tokenize(textual_data.lower())
        frequency_distribution = FreqDist(tokens)
        return frequency_distribution.most_common(int(number_of_words_to_return))

    @classmethod
    def get_nouns(cls, textual_data):
        """
        This function is used to extract nouns from the submitted textual information.
        Noun types: - NN  noun, singular 'desk'
                    - NNS noun plural	'desks'
                    - NNP	proper noun, singular 'Harrison'
                    - NNPS proper noun, plural 'Americans'
        :param textual_data: Textual information
        :return: nouns extracted using NLTK Part of Speech tagging
        :rtype: list
        """
        tokens = word_tokenize(textual_data.lower())
        words = pos_tag(tokens)
        proper_nouns = sorted(set([word for word, pos in words if pos == 'NN'
                                   or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS']))
        return proper_nouns

    @classmethod
    def get_pronouns(cls, textual_data):
        """
        This function is used to extract pronouns from the submitted textual information.
        Pronoun types: - PRP personal pronoun I, he, she
                       - PRP$ possessive pronoun my, his, hers
        :param textual_data: Textual information
        :return: pronouns extracted using NLTK Part of Speech tagging
        :rtype: list
        """
        tokens = word_tokenize(textual_data.lower())
        words = pos_tag(tokens)
        pronouns = sorted(set([word for word, pos in words if pos == 'PRP' or pos == 'PRP$']))
        return pronouns

    @classmethod
    def get_verbs(cls, textual_data):
        """
        This function is used to extract verbs from the submitted textual information.
        Verb types: - VB verb, base form take
                    - VBD verb, past tense took
                    - VBG verb, gerund/present participle taking
                    - VBN verb, past participle	taken
                    - VBP verb, sing. present, non-3d take
                    - VBZ verb, 3rd person sing. present takes
        :param textual_data: Textual information
        :return: verbs extracted using NLTK Part of Speech tagging
        :rtype: list
        """
        tokens = word_tokenize(textual_data.lower())
        words = pos_tag(tokens)
        verbs = sorted(set([word for word, pos in words
                 if (pos == 'VB' or pos == 'VBD' or pos == 'VBG' or pos == 'VBN' or pos == 'VBP' or pos == 'VBZ')]))
        return verbs

    @classmethod
    def get_adverbs(cls, textual_data):
        """
        This function is used to extract adverbs from the submitted textual information.
        Adverb types: - RB adverb very, silently,
                      - RBR	adverb, comparative	better
                      - RBS	adverb, superlative	best
        :param textual_data: Textual information
        :return: adverbs extracted using NLTK Part of Speech tagging
        :rtype: list
        """
        tokens = word_tokenize(textual_data.lower())
        words = pos_tag(tokens)
        adverbs = sorted(set([word for word, pos in words if (pos == 'RB' or pos == 'RBR' or pos == 'RBS')]))
        return adverbs

    @classmethod
    def get_adjectives(cls, textual_data):
        """
        This function is used to extract adjectives from the submitted textual information.
        Adjective types: - JJ adjective	'big'
                         - JJR adjective, comparative 'bigger'
                         - JJS adjective, superlative 'biggest'
        :param textual_data: Textual information
        :return: adjectives extracted using NLTK Part of Speech tagging
        :rtype: list
        """
        tokens = word_tokenize(textual_data.lower())
        words = pos_tag(tokens)
        adjectives = sorted(set([word for word, pos in words if (pos == 'JJ' or pos == 'JJR' or pos == 'JJS')]))
        return adjectives
