# -*- coding: utf-8 -*-
"""
Scrapbag strings file.
"""
import re
import unicodedata
import html2text
import structlog
from bs4 import BeautifulSoup
from markdown import markdown

logger = structlog.getLogger(__name__)


def clean_text(text):
    """
    Retrieve clean text without markdown sintax or other things.
    """
    if text:
        text = html2text.html2text(clean_markdown(text))
        return re.sub(r'\s+', ' ', text).strip()


def clean_markdown(text):
    """
    Parse markdown sintaxt to html.
    """
    result = text

    if isinstance(text, str):
        result = ''.join(
            BeautifulSoup(markdown(text), 'lxml').findAll(text=True))

    return result


def get_only_words(string):
    """
    Get only words scapping numbers and simbols.
    """
    return re.findall(r"[\w']+", string)


# def strip_accents(s):
#     """
#     Change char with different locale with similar.
#     """
# return ''.join(c for c in unicodedata.normalize('NFD', s) if
# unicodedata.category(c) != 'Mn')

def select_regexp_char(char):
    """
    Select correct regex depending the char
    """
    regexp = '{}'.format(char)

    if not isinstance(char, str) and not isinstance(char, int):
        regexp = ''

    if isinstance(char, str) and not char.isalpha() and not char.isdigit():
        regexp = r"\{}".format(char)

    return regexp


def exclude_chars(text, exclusion=None):
    """
    Clean text string of simbols in exclusion list.
    """
    exclusion = [] if exclusion is None else exclusion
    regexp = r"|".join([select_regexp_char(x) for x in exclusion]) or r''
    return re.sub(regexp, '', text)


def strip_accents(text):
    """
    Strip agents from a string.
    """

    normalized_str = unicodedata.normalize('NFD', text)

    return ''.join([
        c for c in normalized_str if unicodedata.category(c) != 'Mn'])


OPERATIONS_EXCLUSION = ['+', '*', '%', '//']


def normalizer(text, exclusion=None, lower=True):
    """
    Clean text string of simbols only alphanumeric chars.
    """

    exclusion = OPERATIONS_EXCLUSION if exclusion is None else exclusion
    clean_str = re.sub(r'[^\w{}]'.format(
        "".join(exclusion)), '-', text.strip()) or ''
    clean_str_without_accents = strip_accents(clean_str)
    limit_guion = re.sub(r'\-+', '-', clean_str_without_accents.strip())

    # TODO: refactor with a regexp
    if limit_guion and '-' in limit_guion[0]:
        limit_guion = limit_guion[1:]

    if limit_guion and '-' in limit_guion[-1]:
        limit_guion = limit_guion[:-1]

    if lower:
        limit_guion = limit_guion.lower()

    return limit_guion


def normalize_dict(dictionary):
    """
    Given an dict, normalize all of their keys using normalize function.
    """
    result = {}
    if isinstance(dictionary, dict):
        keys = list(dictionary.keys())
        for key in keys:
            result[normalizer(key)] = normalize_dict(dictionary.pop(key))
    else:
        result = dictionary
    return result
