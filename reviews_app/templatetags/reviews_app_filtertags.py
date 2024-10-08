import random
from django import template

register = template.Library()


@register.filter
def random_color(_):
    colors = ['#00d1b2', '#23d160', '#ff3860', '#3273dc', '#209cee', '#363636']
    return random.choice(colors)