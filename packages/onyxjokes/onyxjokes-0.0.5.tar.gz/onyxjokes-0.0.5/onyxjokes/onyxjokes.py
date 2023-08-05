from __future__ import absolute_import
import random

from .jokes_en import jokes_en
from .jokes_de import jokes_de
from .jokes_es import jokes_es
from .jokes_fr import jokes_fr

all_jokes = {
    'en-US': jokes_en,
    'de-DE': jokes_de,
    'es-ES': jokes_es,
    'fr-FR': jokes_fr,
}


class LanguageNotFoundError(Exception):
    pass


class CategoryNotFoundError(Exception):
    pass


def get_jokes(language='en-US', category='neutral'):


    if language not in all_jokes:
        raise LanguageNotFoundError('No such language %s' % language)

    jokes = all_jokes[language]

    if category not in jokes:
        raise CategoryNotFoundError('No such category %s in language %s' % (category, language))

    return jokes[category]


def get_joke(language='en-US', category='neutral'):


    jokes = get_jokes(language, category)
    return random.choice(jokes)
