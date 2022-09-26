from django import template
import re

from ..models import Category

register = template.Library()

CURSE_WORDS = ['хуй', 'пизда', 'ебать', 'блядь']                # list of unwanted words


@register.filter()
def censor(string):                                             # modify string aka censor above words
    try:
        for word in CURSE_WORDS:
            if word in string.lower():

                # Here we substitute the curse word with appropriate amount of *
                # It replaces the substring that matches the word rather than the standing alone curse word
                # we can use replace two times, but I believe this one is faster as it goes through string only once
                string = re.sub(f'{word}|{word.capitalize()}',
                                lambda match: match.group()[:1] + "*" * len(match.group()[1:]),
                                string)

    except AttributeError as e:
        print(e)

    return string


@register.filter()
def get_attribute(querydict, attr):                 # get attributes list from request.GET key
    return querydict.getlist(attr)



@register.filter()
def get_attr_model(pk, attr):                       # get model via pk
    if attr == 'category':
        # pk is transfered as list with length 1
        return Category.objects.get(pk=pk[0])

    else:
        return 'No such model'
